import { memo } from "react";

function TypingIndicatorComponent() {
  return (
    <div className="typing" role="status" aria-live="polite" aria-label="Assistant is typing">
      <span className="sr-only">Assistant is typing…</span>
      <span className="typing__dot" aria-hidden="true" />
      <span className="typing__dot" aria-hidden="true" />
      <span className="typing__dot" aria-hidden="true" />
    </div>
  );
}

const TypingIndicator = memo(TypingIndicatorComponent);
export default TypingIndicator;
