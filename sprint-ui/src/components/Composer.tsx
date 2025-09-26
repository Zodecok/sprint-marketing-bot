import { forwardRef } from "react";

type ComposerProps = {
  value: string;
  onChange: (value: string) => void;
  onSubmit: () => void;
  placeholder?: string;
  disabled?: boolean;
  ariaLabel: string;
  onFocus?: () => void;
  onBlur?: () => void;
};

const Composer = forwardRef<HTMLTextAreaElement, ComposerProps>(function Composer(
  { value, onChange, onSubmit, placeholder, disabled, ariaLabel, onFocus, onBlur },
  ref,
) {
  return (
    <form
      className="chat-composer"
      onSubmit={(event) => {
        event.preventDefault();
        onSubmit();
      }}
    >
      <label className="sr-only" htmlFor="chat-input">
        {ariaLabel}
      </label>
      <textarea
        id="chat-input"
        ref={ref}
        value={value}
        placeholder={placeholder}
        aria-label={ariaLabel}
        className="chat-composer__input"
        disabled={disabled}
        rows={1}
        maxLength={2000}
        onChange={(event) => onChange(event.target.value)}
        onFocus={onFocus}
        onBlur={onBlur}
        onKeyDown={(event) => {
          if (event.key === "Enter" && !event.shiftKey) {
            event.preventDefault();
            onSubmit();
          }
        }}
      />
      <button
        type="submit"
        className="chat-composer__send"
        aria-label="Send message"
        disabled={disabled || !value.trim()}
      >
        <SendIcon />
      </button>
    </form>
  );
});

export default Composer;

function SendIcon() {
  return (
    <svg
      className="chat-composer__send-icon"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
    >
      <path strokeLinecap="round" strokeLinejoin="round" d="M5 12h6m0 0 10-7-10 14V12Z" />
    </svg>
  );
}
