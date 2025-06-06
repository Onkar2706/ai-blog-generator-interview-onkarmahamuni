from flask import Flask, request, jsonify
from seo_fetcher import fetch_seo_metrics
from ai_generator import generate_blog_post
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = Flask(__name__)

# --- Main Endpoint ---
@app.route('/generate')
def generate():
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({'error': 'Keyword is required'}), 400

    seo = fetch_seo_metrics(keyword)
    post = generate_blog_post(keyword, seo)

    filename = f"generated_{keyword.replace(' ', '_')}.md"
    with open(filename, "w") as f:
        f.write(post)

    return jsonify({
        "keyword": keyword,
        "seo": seo,
        "blog_post_file": filename
    })


# --- Optional: Scheduler to generate daily ---
def scheduled_job():
    keyword = "wireless earbuds"
    seo = fetch_seo_metrics(keyword)
    post = generate_blog_post(keyword, seo)

    filename = f"daily_{keyword.replace(' ', '_')}.md"
    with open(filename, "w") as f:
        f.write(post)
    print(f"Saved: {filename}")

scheduler = BackgroundScheduler()
scheduler.add_job(scheduled_job, 'interval', days=1)
scheduler.start()


if __name__ == "__main__":
    app.run(debug=True)

