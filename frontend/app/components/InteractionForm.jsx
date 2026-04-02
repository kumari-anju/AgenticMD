'use client';

/**
 * InteractionForm — Left panel
 * Read-only form populated exclusively by the AI assistant.
 * Matches the reference UI layout.
 */
export default function InteractionForm({ formState, changedFields }) {
  const {
    hcp_name,
    date,
    interaction_type,
    sentiment,
    shared_materials,
    topic_discussed,
    time,
  } = formState;

  const isHighlighted = (field) =>
    changedFields.includes(field) ? 'highlighted' : '';

  // Format materials list for display
  const materialsText =
    shared_materials && shared_materials.length > 0
      ? shared_materials.join(', ') + '.'
      : null;

  return (
    <div className="form-panel" id="interaction-form-panel">
      <h1 className="form-title">Log HCP Interaction</h1>

      {/* ── Interaction Details ── */}
      <h2 className="form-section-title">Interaction Details</h2>

      <div className="form-row">
        <div className="form-group">
          <label className="form-label">HCP Name</label>
          <input
            type="text"
            className={`form-input ${hcp_name ? 'has-value' : ''} ${isHighlighted('hcp_name')}`}
            value={hcp_name || ''}
            placeholder="Search or select HCP..."
            readOnly
            disabled
            id="field-hcp-name"
          />
        </div>
        <div className="form-group">
          <label className="form-label">Interaction Type</label>
          <div className={`form-select ${isHighlighted('interaction_type')}`}>
            {interaction_type || 'Meeting'}
          </div>
        </div>
      </div>

      <div className="form-row">
        <div className="form-group">
          <label className="form-label">Date</label>
          <div className="form-input-icon">
            <input
              type="text"
              className={`form-input ${date ? 'has-value' : ''} ${isHighlighted('date')}`}
              value={date || ''}
              placeholder="MM/DD/YYYY"
              readOnly
              disabled
              id="field-date"
            />
            <span className="icon">📅</span>
          </div>
        </div>
        <div className="form-group">
          <label className="form-label">Time</label>
          <div className="form-input-icon">
            <input
              type="text"
              className={`form-input ${time ? 'has-value' : ''} ${isHighlighted('time')}`}
              value={time || ''}
              placeholder="HH:MM PM"
              readOnly
              disabled
              id="field-time"
            />
            <span className="icon">🕐</span>
          </div>
        </div>
      </div>

      {/* ── Attendees ── */}
      <div className="form-row single">
        <div className="form-group">
          <label className="form-label">Attendees</label>
          <input
            type="text"
            className="form-input"
            value=""
            placeholder="Enter names or search..."
            readOnly
            disabled
            id="field-attendees"
          />
        </div>
      </div>

      {/* ── Topics Discussed ── */}
      <div className="form-group">
        <label className="form-label">Topics Discussed</label>
        <textarea
          className={`form-textarea ${isHighlighted('topic_discussed')}`}
          value={topic_discussed || ''}
          placeholder="Enter key discussion points..."
          readOnly
          disabled
          id="field-topics"
        />
      </div>

      <span className="voice-note-link">
        <span className="link-icon">🎙️</span>
        Summarize from Voice Note (Requires Consent)
      </span>

      {/* ── Materials Shared / Samples Distributed ── */}
      <div className="materials-section">
        <h3 className="materials-header">Materials Shared / Samples Distributed</h3>

        <div className="materials-sub-header">Materials Shared</div>
        <div className={`materials-content ${isHighlighted('shared_materials')}`}>
          <span className={`materials-text ${materialsText ? 'has-value' : ''}`}>
            {materialsText || 'No materials added.'}
          </span>
          <button className="materials-btn" disabled>
            <span className="btn-icon">🔍</span> Search/Add
          </button>
        </div>
      </div>

      <div className="materials-section">
        <div className="materials-sub-header">Samples Distributed</div>
        <div className="materials-content">
          <span className="materials-text">No samples added.</span>
          <button className="materials-btn" disabled>
            <span className="btn-icon">+</span> Add Sample
          </button>
        </div>
      </div>

      {/* ── Sentiment ── */}
      <div className="form-group">
        <label className="form-label">Observed/Inferred HCP Sentiment</label>
        <div className="sentiment-group" id="field-sentiment">
          {['Positive', 'Neutral', 'Negative'].map((option) => {
            const emoji =
              option === 'Positive'
                ? '😊'
                : option === 'Neutral'
                  ? '😐'
                  : '😟';
            const isSelected =
              sentiment &&
              sentiment.toLowerCase() === option.toLowerCase();

            return (
              <div
                key={option}
                className={`sentiment-option ${isSelected && isHighlighted('sentiment') ? 'highlighted' : ''}`}
              >
                <div
                  className={`sentiment-radio ${isSelected ? 'selected' : ''}`}
                />
                <span className="sentiment-emoji">{emoji}</span>
                <span className="sentiment-label">{option}</span>
              </div>
            );
          })}
        </div>
      </div>

      {/* ── Outcomes ── */}
      <div className="form-group">
        <label className="form-label">Outcomes</label>
        <textarea
          className="form-textarea"
          value=""
          placeholder="Key outcomes or agreements..."
          readOnly
          disabled
          id="field-outcomes"
        />
      </div>

      {/* ── Follow-up Actions ── */}
      <div className="form-group">
        <label className="form-label">Follow-up Actions</label>
        <textarea
          className="form-textarea"
          value=""
          placeholder="Planned follow-up actions..."
          readOnly
          disabled
          id="field-followup"
        />
      </div>
    </div>
  );
}
