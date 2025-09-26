import { useState } from "react";
import { useNavigate } from "react-router-dom";
import client from "../api/client";
import HelpTooltip from "../components/HelpTooltip";

const emptyState = {
  title: "",
  specialty: "",
  difficulty: "Easy",
  rubric_id: "",
  objectives: [""],
  patient: {
    demographics: { age: "", sex: "" },
    personality: "",
    baseline_vitals: { temp_c: "", hr: "", rr: "", bp: "" },
    core_story: { chief_complaint: "", hpi_summary: "" },
  },
  qa_reveals: {},           // { key: value }
  orders: { allowed: [""], results: {} }, // results: { testName: resultText }
  expected: {
    key_findings: [""],
    differentials: { should_include: [""], reasonable_alternatives: [""] },
    final_dx: "",
    initial_plan_high_level: [""],
  },
};

export default function CaseBuilder() {
  const [form, setForm] = useState(emptyState);
  const [submitting, setSubmitting] = useState(false);
  const navigate = useNavigate();

  const set = (path, value) => {
    setForm(prev => {
      const clone = structuredClone(prev);
      const segs = path.split(".");
      let cur = clone;
      for (let i = 0; i < segs.length - 1; i++) cur = cur[segs[i]];
      cur[segs.at(-1)] = value;
      return clone;
    });
  };

  const addToList = (path) => set(path, [...pathGet(form, path), ""]);
  const removeFromList = (path, idx) => {
    const list = [...pathGet(form, path)];
    list.splice(idx, 1);
    set(path, list.length ? list : [""]);
  };
  const updateListItem = (path, idx, value) => {
    const list = [...pathGet(form, path)];
    list[idx] = value;
    set(path, list);
  };

  const setKV = (objPath, k, v) => {
    const obj = { ...pathGet(form, objPath) };
    if (!k && !v) return;
    obj[k] = v;
    set(objPath, obj);
  };
  const removeKV = (objPath, k) => {
    const obj = { ...pathGet(form, objPath) };
    delete obj[k];
    set(objPath, obj);
  };

  const onSubmit = async (e) => {
    e.preventDefault();
    if (!form.title || !form.rubric_id) {
      alert("Title and Rubric ID are required.");
      return;
    }
    setSubmitting(true);
    try {
      // Send structured JSON; backend will generate YAML
      await client.post("/cases/", form);
      navigate("/cases"); // back to list
    } catch (err) {
      console.error(err);
      alert("Failed to create case.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold text-gray-700">Create New Case</h1>
        <button
          onClick={() => navigate("/cases")}
          className="bg-white text-blue-600 px-3 py-1 rounded hover:bg-gray-200 transition"
        >
          ← Back
        </button>
      </div>

      <form onSubmit={onSubmit} className="space-y-8">
        {/* Basics */}
        <section className="bg-white p-5 rounded-xl shadow border space-y-4">
          <h2 className="text-lg font-semibold text-gray-700">Basics</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input label={
            <>
              Title * <HelpTooltip text="The display name of the case, e.g. 'Dysuria and frequency in a young adult'." />     
             </>
            } 
            value={form.title} onChange={(v) => set("title", v)} />
            <Input label={
              <>
              Rubric ID * <HelpTooltip text="ID of the rubric used to evaluate this case. Must match an existing rubric."/>
              </>
            } 
            value={form.rubric_id} onChange={(v) => set("rubric_id", v)} />
            <Input label={
              <>
              Specialty <HelpTooltip text="The medical specialty this case belongs to, e.g. Family Medicine, Cardiology."/>
              </>}
              value={form.specialty} onChange={(v) => set("specialty", v)} />
            <Select
              label="Difficulty"
              value={form.difficulty}
              onChange={(v) => set("difficulty", v)}
              options={["Easy", "Medium", "Hard"]}
            />
          </div>

          <ListEditor
            label={
              <>
                Objectives{" "}
                <HelpTooltip text="Learning goals the student should achieve while working on this case." />
              </>
            }
            items={form.objectives}
            onAdd={() => addToList("objectives")}
            onRemove={(i) => removeFromList("objectives", i)}
            onChange={(i, v) => updateListItem("objectives", i, v)}
          />
        </section>

        {/* Patient */}
        <section className="bg-white p-5 rounded-xl shadow border space-y-4">
          <h2 className="text-lg font-semibold text-gray-700">Patient</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Input label={<>Age <HelpTooltip text="Patient's age in years." /></>} value={form.patient.demographics.age} onChange={(v) => set("patient.demographics.age", v)} />
            <Input label={<>Sex <HelpTooltip text="Biological sex of the patient (male/female)." /></>} value={form.patient.demographics.sex} onChange={(v) => set("patient.demographics.sex", v)} />
            <Input label={<>Personality <HelpTooltip text="General demeanor of the patient (e.g. cooperative, anxious)." /></>} value={form.patient.personality} onChange={(v) => set("patient.personality", v)} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <Input label={<>Temp (°C) <HelpTooltip text="Baseline body temperature." /></>} value={form.patient.baseline_vitals.temp_c} onChange={(v) => set("patient.baseline_vitals.temp_c", v)} />
            <Input label={<>HR <HelpTooltip text="Baseline heart rate (beats per minute)." /></>} value={form.patient.baseline_vitals.hr} onChange={(v) => set("patient.baseline_vitals.hr", v)} />
            <Input label={<>RR <HelpTooltip text="Baseline respiratory rate (breaths per minute)." /></>} value={form.patient.baseline_vitals.rr} onChange={(v) => set("patient.baseline_vitals.rr", v)} />
            <Input label={<>BP <HelpTooltip text="Baseline blood pressure (systolic/diastolic)." /></>} value={form.patient.baseline_vitals.bp} onChange={(v) => set("patient.baseline_vitals.bp", v)} />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <Input label={<>Chief Complaint <HelpTooltip text="The main symptom or problem the patient reports." /></>} value={form.patient.core_story.chief_complaint} onChange={(v) => set("patient.core_story.chief_complaint", v)} />
            <TextArea label={<>HPI Summary <HelpTooltip text="Summary of the history of present illness (patient’s narrative of their symptoms)." /></>} value={form.patient.core_story.hpi_summary} onChange={(v) => set("patient.core_story.hpi_summary", v)} />
          </div>
        </section>

        {/* Q&A Reveals */}
        <section className="bg-white p-5 rounded-xl shadow border space-y-4">
          <h2 className="text-lg font-semibold text-gray-700">Q&A Reveals</h2>

          <label className="block text-sm text-gray-700 mb-1">
            Pre-scripted Answers{" "}
            <HelpTooltip text="Define question → answer pairs. Example: 'When did this start?' → 'Three days ago'." />
          </label>

          <KVEditor
            obj={form.qa_reveals}
            onAdd={(k, v) => setKV("qa_reveals", k, v)}
            onRemove={(k) => removeKV("qa_reveals", k)}
          />
        </section>

        {/* Orders */}
        <section className="bg-white p-5 rounded-xl shadow border space-y-4">
          <h2 className="text-lg font-semibold text-gray-700">Orders</h2>

          <ListEditor
            label={<>Allowed Tests <HelpTooltip text="List of diagnostic tests the student is permitted to order." /></>}
            items={form.orders.allowed}
            onAdd={() => addToList("orders.allowed")}
            onRemove={(i) => removeFromList("orders.allowed", i)}
            onChange={(i, v) => updateListItem("orders.allowed", i, v)}
          />

          <h3 className="font-medium flex items-center gap-1 text-gray-600">
            Results (per test) <HelpTooltip text="Expected results for each test. Keys must match an allowed test." />
          </h3>
          <KVEditor
            obj={form.orders.results}
            onAdd={(k, v) => setKV("orders.results", k, v)}
            onRemove={(k) => removeKV("orders.results", k)}
            keyPlaceholder="Test name (must match allowed)"
            valuePlaceholder="Result text"
          />
        </section>

        {/* Expected */}
        <section className="bg-white p-5 rounded-xl shadow border space-y-4">
          <h2 className="text-lg font-semibold text-gray-700">Expected</h2>

          <ListEditor
            label={<>Key Findings <HelpTooltip text="Important clinical findings that should be elicited during the encounter." /></>}
            items={form.expected.key_findings}
            onAdd={() => addToList("expected.key_findings")}
            onRemove={(i) => removeFromList("expected.key_findings", i)}
            onChange={(i, v) => updateListItem("expected.key_findings", i, v)}
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <ListEditor
              label={<>Differentials: Should Include <HelpTooltip text="Critical diagnoses that must appear in the student's differential diagnosis." /></>}
              items={form.expected.differentials.should_include}
              onAdd={() => addToList("expected.differentials.should_include")}
              onRemove={(i) => removeFromList("expected.differentials.should_include", i)}
              onChange={(i, v) => updateListItem("expected.differentials.should_include", i, v)}
            />
            <ListEditor
              label={<>Differentials: Reasonable Alternatives <HelpTooltip text="Other diagnoses that could reasonably be considered but are not required." /></>}
              items={form.expected.differentials.reasonable_alternatives}
              onAdd={() => addToList("expected.differentials.reasonable_alternatives")}
              onRemove={(i) => removeFromList("expected.differentials.reasonable_alternatives", i)}
              onChange={(i, v) => updateListItem("expected.differentials.reasonable_alternatives", i, v)}
            />
          </div>

          <Input label={<>Final Diagnosis <HelpTooltip text="The correct final diagnosis for this case." /></>} value={form.expected.final_dx} onChange={(v) => set("expected.final_dx", v)} />

          <ListEditor
            label={<>Initial Plan (High Level) <HelpTooltip text="High-level management plan: outpatient vs inpatient, education, safety netting, etc." /></>}
            items={form.expected.initial_plan_high_level}
            onAdd={() => addToList("expected.initial_plan_high_level")}
            onRemove={(i) => removeFromList("expected.initial_plan_high_level", i)}
            onChange={(i, v) => updateListItem("expected.initial_plan_high_level", i, v)}
          />
        </section>

        <div className="flex items-center gap-3">
          <button
            type="submit"
            disabled={submitting}
            className="px-4 py-2 rounded bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-60"
          >
            {submitting ? "Creating..." : "Create Case"}
          </button>
          <button
            type="button"
            onClick={() => setForm(emptyState)}
            className="px-4 py-2 rounded bg-gray-100 hover:bg-gray-200"
          >
            Reset
          </button>
        </div>
      </form>
    </div>
  );
}

/* ---------------- UI Helpers ---------------- */

function Input({ label, value, onChange, type="text" }) {
  return (
    <label className="block">
      <span className="text-sm text-gray-700">{label}</span>
      <input
        type={type}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="mt-1 w-full border rounded px-3 py-2"
      />
    </label>
  );
}

function TextArea({ label, value, onChange }) {
  return (
    <label className="block">
      <span className="text-sm text-gray-700">{label}</span>
      <textarea
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="mt-1 w-full border rounded px-3 py-2 min-h-[110px]"
      />
    </label>
  );
}

function Select({ label, value, onChange, options }) {
  return (
    <label className="block">
      <span className="text-sm text-gray-700">{label}</span>
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="mt-1 w-full border rounded px-3 py-2"
      >
        {options.map(opt => <option key={opt} value={opt}>{opt}</option>)}
      </select>
    </label>
  );
}

function ListEditor({ label, items, onAdd, onRemove, onChange }) {
  return (
    <div className="space-y-2">
      <div className="flex items-center justify-between">
        <span className="text-sm text-gray-700">{label}</span>
        <button type="button" onClick={onAdd} className="bg-white text-blue-600 px-3 py-1 rounded hover:bg-gray-200 transition">+ Add</button>
      </div>
      <div className="space-y-2">
        {items.map((value, i) => (
          <div className="flex gap-2" key={i}>
            <input
              value={value}
              onChange={(e) => onChange(i, e.target.value)}
              className="flex-1 border rounded px-3 py-2"
            />
            <button type="button" onClick={() => onRemove(i)} className="px-2 py-1 rounded bg-red-50 hover:bg-red-100 text-red-600">Remove</button>
          </div>
        ))}
      </div>
    </div>
  );
}

function KVEditor({ obj, onAdd, onRemove, keyPlaceholder="Key", valuePlaceholder="Value" }) {
  // transient local fields for adding a pair
  const [k, setK] = useState("");
  const [v, setV] = useState("");

  return (
    <div className="space-y-3">
      <div className="flex gap-2">
        <input value={k} onChange={(e) => setK(e.target.value)} placeholder={keyPlaceholder} className="flex-1 border rounded px-3 py-2" />
        <input value={v} onChange={(e) => setV(e.target.value)} placeholder={valuePlaceholder} className="flex-1 border rounded px-3 py-2" />
        <button type="button" onClick={() => { onAdd(k, v); setK(""); setV(""); }} className="bg-white text-blue-600 px-3 py-1 rounded hover:bg-gray-200 transition">Add</button>
      </div>
      <div className="space-y-2">
        {Object.entries(obj).map(([key, val]) => (
          <div key={key} className="flex gap-2 items-center">
            <div className="flex-1 border rounded px-3 py-2 bg-gray-50">{key}</div>
            <div className="flex-[2] border rounded px-3 py-2">{val}</div>
            <button type="button" onClick={() => onRemove(key)} className="px-2 py-1 rounded bg-red-50 hover:bg-red-100 text-red-600">Remove</button>
          </div>
        ))}
      </div>
    </div>
  );
}

/* Utility to get nested path (read-only) */
function pathGet(obj, path) {
  return path.split(".").reduce((acc, seg) => acc?.[seg], obj);
}
