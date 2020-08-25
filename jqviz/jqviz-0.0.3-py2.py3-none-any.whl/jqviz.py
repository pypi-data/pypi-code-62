import click
import subprocess
import os
import webbrowser
import asyncio

from flask import Flask, render_template, redirect, url_for, request, session
app = Flask(__name__)
app.secret_key = "soTjK_UgaHcK8HM4nBTwFv.UvzMcNxyPXKnH_TWYoZ@Dc.*PdKxVs.kaCTtJ-UXZ"

@app.route('/')
def index():
    filename = os.environ["JQ_FILENAME"]
    jq_filter = session.get("filter", ".")
    print(f"jq_filter: {jq_filter}")
    try:
        output = subprocess.check_output(["jq", jq_filter, filename]).decode()
    except subprocess.CalledProcessError as jq_err:
        output = jq_err.output.decode()
    return render_template("index.html", json=output, filename=filename, filter=jq_filter)

@app.route('/update-filter', methods=['POST'])
def update_filter():
    session["filter"] = request.form["jq_filter"]
    return redirect(url_for("index"))

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return "<p>Server shutting down...</p><p>Feel free to close this window</p>"

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

async def start_flask():
    # subprocess.check_call(["flask", "run"], stdout=subprocess.DEVNULL)
    process = await asyncio.create_subprocess_shell("flask run", stdout=asyncio.subprocess.PIPE)
    stdout, stderr = await process.communicate()

async def open_browser_window(port):
    await asyncio.sleep(1)
    webbrowser.open(f"http://127.0.0.1:{ port }/")

async def setup_and_run_server(port):
    await asyncio.gather(open_browser_window(port), start_flask())


@click.command()
@click.argument('filename', type=click.Path(exists=True))
@click.option('--port', default=5000, help="Port on which to run the Flask server")
def main(filename, port):
    os.environ["FLASK_APP"] = __file__
    os.environ["JQ_FILENAME"] = filename
    asyncio.run(setup_and_run_server(port))


if __name__ == "__main__":
    main()