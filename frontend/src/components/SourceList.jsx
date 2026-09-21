function SourceList({ sources }) {
  if (!sources?.length) {
    return null;
  }

  return (
    <div className="source-list">
      <div className="source-heading">
        <span className="source-rule" />
        <span>Referenced pages</span>
      </div>
      <div className="source-items">
        {sources.map((item, index) => (
          <div className="source-item" key={`${item.source}-${item.page}-${index}`}>
            <span className="source-number">{String(index + 1).padStart(2, "0")}</span>
            <span className="source-name">{item.source}</span>
            <span className="source-page">Page {item.page}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default SourceList;