import Chat from "./components/Chat";

function App() {
  return (
    <main className="app-shell">
      <div className="paper-texture" aria-hidden="true" />
      <header className="site-header">
        <a className="brand" href="/" aria-label="Knowledge Desk home">
          <span className="brand-mark">K</span>
          <span>Knowledge Desk</span>
        </a>
        <span className="status-pill">
          <span className="status-dot" />
          <span>Document index online</span>
        </span>
      </header>

      <section className="intro" aria-labelledby="page-title">
        <p className="eyebrow">Your private reading room</p>
        <h1 id="page-title">Ask the<br /><em>documents.</em></h1>
        <p className="intro-copy">
          Search across your PDF library with answers grounded in the pages that matter.
        </p>
      </section>

      <Chat />

      <footer className="site-footer">
        <span>RAG / semantic search</span>
        <span>Sources stay attached to every answer</span>
      </footer>
    </main>
  );
}

export default App;