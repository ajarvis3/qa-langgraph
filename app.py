"""Flask application entry point for qa-langgraph."""

import logging
import os

from flask import Flask, jsonify, request

from agent import run_agent

app = Flask(__name__)
logger = logging.getLogger(__name__)


@app.route("/run", methods=["POST"])
def run():
    """Run a LangGraph agent.

    Expects a multipart/form-data request with:
      - query  (str, required): The question or instruction for the agent.
      - file   (file, required): A plain-text file whose contents serve as the
                                 agent's system prompt / definition.  An empty
                                 file is accepted; the agent will run without a
                                 system prompt in that case.

    Returns a JSON object with a single ``result`` key containing the agent's
    response, or an ``error`` key with a description of what went wrong.
    """
    query = request.form.get("query", "").strip()
    if not query:
        return jsonify({"error": "Missing required field: query"}), 400

    agent_file = request.files.get("file")
    if agent_file is None:
        return jsonify({"error": "Missing required field: file"}), 400

    try:
        agent_definition = agent_file.read().decode("utf-8")
    except Exception as exc:
        logger.warning("Could not read agent file: %s", exc)
        return jsonify({"error": "Could not read agent file"}), 400

    try:
        answer = run_agent(query=query, agent_definition=agent_definition)
    except Exception as exc:
        logger.exception("Agent execution failed: %s", exc)
        return jsonify({"error": "Agent execution failed"}), 500

    return jsonify({"result": answer})


if __name__ == "__main__":
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    app.run(debug=debug)
