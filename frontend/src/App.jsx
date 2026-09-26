function App() {
  return (
    <div className="app">

      <header>
        <h1>Smriti</h1>
        <p>Sovereign Team Memory</p>
      </header>

      <section className="stats">

        <div className="card">
          <h2>23</h2>
          <p>Memories</p>
        </div>

        <div className="card">
          <h2>5</h2>
          <p>Commitments</p>
        </div>

        <div className="card">
          <h2>2</h2>
          <p>Conflicts</p>
        </div>

        <div className="card">
          <h2>1</h2>
          <p>Overdue</p>
        </div>

      </section>

      <section className="ask">

        <h2>Ask Smriti</h2>

        <input
          type="text"
          placeholder="Ask about a decision, commitment or deadline..."
        />

        <button>Ask Smriti</button>

      </section>

      <section className="content">

        <div className="panel">
          <h2>Recent Commitments</h2>

          <p>
            <strong>Rohan</strong> ΓÇö Poster
          </p>

          <p>
            <strong>Akash</strong> ΓÇö Sponsorship deck
          </p>

        </div>

        <div className="panel">
          <h2>Recent Decisions</h2>

          <p>
            Venue changed to Hall B
          </p>

          <p>
            Auditorium unavailable on August 28
          </p>

        </div>

      </section>

    </div>
  );
}

export default App;
