import React from "react";

interface Props {
  onShare: () => void;
}

const ResponseSharing: React.FC<Props> = ({ onShare }) => {
  return (
    <div className="response-sharing">
      <button onClick={onShare}>Share Response</button>
    </div>
  );
};

export default ResponseSharing;
