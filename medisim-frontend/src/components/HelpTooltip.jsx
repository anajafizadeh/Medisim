export default function HelpTooltip({ text }) {
  return (
    <span className="relative inline-block ml-1 group">
      <span className="w-4 h-4 inline-flex items-center justify-center rounded-full bg-gray-400 text-xs font-bold text-white cursor-pointer">
        ?
      </span>
      <span className="absolute left-5 top-1/2 -translate-y-1/2 w-56 p-2 bg-gray-800 text-white text-sm rounded shadow-lg opacity-0 group-hover:opacity-100 transition pointer-events-none z-10">
        {text}
      </span>
    </span>
  );
}