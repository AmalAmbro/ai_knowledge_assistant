import { useState } from "react";


export default function IngestForm() {
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);

  const handleIngest = async () => {
    if (!text.trim()) {
      setResult("Text is empty");
      return;
    }

    setLoading(true);
    setResult(null);

		try {
			const res = await fetch(
				`http://localhost:8000/ingest`,
				{ 
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({text}),
        }
			);

			if (!res.ok) throw new Error("Ingest failed");

			const data = await res.json();
			setResult(`${data.chunks_added} chunks added`);
			setText("");
		} catch (err) {
			console.error(err);
			setResult("Failed to ingest text");
		} finally {
      setLoading(false);
    }
	};

  return (
    <div>
      <h2>Ingest Knowledge</h2>

      <textarea
        placeholder="Paste text to ingest..."
        value={text}
        onChange={(e) => setText(e.target.value)}
      />

      <button onClick={handleIngest} disabled={loading}>
        {loading ? "Ingesting..." : "Ingest"}
      </button>

      {result && (
        <p className={`result ${result.includes("Chunks added") ? "success" : "error"}`}>
          {result}
        </p>
      )}
    </div>
  );
}
