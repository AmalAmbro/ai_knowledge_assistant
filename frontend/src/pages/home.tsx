import IngestForm from "../components/IngestForm";
import ChatBox from "../components/ChatBox";
import FileUpload from "../components/FileUpload";


export default function App() {
  return (
    <>
      <div className="container">
        <h1>AI Knowledge Assistant</h1>

        <div className="card">
          <IngestForm />
        </div>

        <div className="card">
          <FileUpload />
        </div>

        <div className="card">
          <ChatBox />
        </div>
      </div>
    </>
  );
}
