type Props = {
  sourceType: string;
};

function getBadgeStyle(sourceType: string) {
  switch (sourceType) {
    case "REFERRAL":
      return "bg-green-500/20 text-green-300";

    case "MANUAL":
      return "bg-slate-500/20 text-slate-300";

    case "EXTERNAL":
      return "bg-purple-500/20 text-purple-300";

    case "OPPORTUNITY":
      return "bg-blue-500/20 text-blue-300";

    default:
      return "bg-slate-600/20 text-slate-300";
  }
}

export function ApplicationSourceBadge({ sourceType }: Props) {
  return (
    <span
      className={`rounded-full px-3 py-1 text-xs font-semibold ${getBadgeStyle(
        sourceType,
      )}`}>
      {sourceType}
    </span>
  );
}
