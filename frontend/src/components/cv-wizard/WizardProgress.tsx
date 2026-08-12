type WizardStep = {
  id: string;
  label: string;
};

type Props = {
  currentStep: string;
};

const steps: WizardStep[] = [
  {
    id: "upload",
    label: "Upload",
  },
  {
    id: "analysis",
    label: "Analysis",
  },
  {
    id: "review",
    label: "Review",
  },
  {
    id: "summary",
    label: "Summary",
  },
];

export function WizardProgress({ currentStep }: Props) {
  const currentStepIndex = steps.findIndex((step) => step.id === currentStep);

  return (
    <div className="mb-6">
      <div className="flex items-center justify-between gap-2">
        {steps.map((step, index) => {
          const isActive = step.id === currentStep;
          const isCompleted = currentStepIndex > index;

          return (
            <div key={step.id} className="flex flex-1 items-center gap-2">
              <div
                className={[
                  "flex h-8 w-8 items-center justify-center rounded-full border text-sm font-semibold",
                  isActive ? "border-blue-500 bg-blue-600 text-white" : "",
                  isCompleted ? "border-green-500 bg-green-600 text-white" : "",
                  !isActive && !isCompleted
                    ? "border-slate-700 bg-slate-950 text-slate-500"
                    : "",
                ].join(" ")}>
                {index + 1}
              </div>

              <div className="hidden text-sm md:block">
                <p
                  className={
                    isActive || isCompleted
                      ? "text-slate-200"
                      : "text-slate-500"
                  }>
                  {step.label}
                </p>
              </div>

              {index < steps.length - 1 && (
                <div
                  className={
                    isCompleted
                      ? "h-px flex-1 bg-green-600"
                      : "h-px flex-1 bg-slate-800"
                  }
                />
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}
