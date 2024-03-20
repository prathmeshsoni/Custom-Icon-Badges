import requests
from flask import Flask, render_template, Response, request, redirect

app = Flask(__name__)


# Redirect to a specific URL for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return redirect('https://prathmeshsoni.works')


# Disable cache for the image
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    response.headers['Last-Modified'] = '0'
    return response


# Increment the file and return the current number
def increment_file(filename):
    try:
        with open(filename, 'r+') as file:
            count = int(file.read() or 0) + 1
            file.seek(0)
            file.truncate()
            file.write(str(count))
    except FileNotFoundError:
        count = 1
        with open(filename, 'w') as file:
            file.write(str(count))
    return count


# Shorten large numbers
def short_number(num):
    units = ['', 'K', 'M', 'B', 'T']
    for i in range(len(units)):
        if abs(num) < 1000.0:
            if int(f'{num:.1f}'.split('.')[-1]) == 0:
                return f"{num}{units[i]}"
            else:
                return f"{num:.1f}{units[i]}"
        num /= 1000.0


# Get contents of a URL with requests
def get_contents(url):
    response = requests.get(url)
    return response.content


@app.route('/')
def home():
    return render_template('index.html')


# Route to generate and display the badge for visitors
@app.route('/github/visitors')
def get_visitors():
    views_count = increment_file("views.txt")
    message = short_number(views_count)
    params = {
        "label": "VISITOR",
        "logo": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGZpbGw9IndoaXRlIiB2ZXJzaW9uPSIxLjEiIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgdmlld0JveD0iMCAwIDE2IDE2IiBjbGFzcz0ib2N0aWNvbiBvY3RpY29uLWV5ZSIgYXJpYS1oaWRkZW49InRydWUiPjxwYXRoIGQ9Ik04IDJjMS45ODEgMCAzLjY3MS45OTIgNC45MzMgMi4wNzggMS4yNyAxLjA5MSAyLjE4NyAyLjM0NSAyLjYzNyAzLjAyM2ExLjYyIDEuNjIgMCAwIDEgMCAxLjc5OGMtLjQ1LjY3OC0xLjM2NyAxLjkzMi0yLjYzNyAzLjAyM0MxMS42NyAxMy4wMDggOS45ODEgMTQgOCAxNGMtMS45ODEgMC0zLjY3MS0uOTkyLTQuOTMzLTIuMDc4QzEuNzk3IDEwLjgzLjg4IDkuNTc2LjQzIDguODk4YTEuNjIgMS42MiAwIDAgMSAwLTEuNzk4Yy40NS0uNjc3IDEuMzY3LTEuOTMxIDIuNjM3LTMuMDIyQzQuMzMgMi45OTIgNi4wMTkgMiA4IDJaTTEuNjc5IDcuOTMyYS4xMi4xMiAwIDAgMCAwIC4xMzZjLjQxMS42MjIgMS4yNDEgMS43NSAyLjM2NiAyLjcxN0M1LjE3NiAxMS43NTggNi41MjcgMTIuNSA4IDEyLjVjMS40NzMgMCAyLjgyNS0uNzQyIDMuOTU1LTEuNzE1IDEuMTI0LS45NjcgMS45NTQtMi4wOTYgMi4zNjYtMi43MTdhLjEyLjEyIDAgMCAwIDAtLjEzNmMtLjQxMi0uNjIxLTEuMjQyLTEuNzUtMi4zNjYtMi43MTdDMTAuODI0IDQuMjQyIDkuNDczIDMuNSA4IDMuNWMtMS40NzMgMC0yLjgyNS43NDItMy45NTUgMS43MTUtMS4xMjQuOTY3LTEuOTU0IDIuMDk2LTIuMzY2IDIuNzE3Wk04IDEwYTIgMiAwIDEgMS0uMDAxLTMuOTk5QTIgMiAwIDAgMSA4IDEwWiI+PC9wYXRoPjwvc3ZnPg==",
        "message": message,
        "color": "purple",
        "style": "for-the-badge",
        "labelColor": "640464",
        "logoColor": "FFFFFF",
    }
    url = "https://img.shields.io/static/v1?" + "&".join(f"{key}={value}" for key, value in params.items())
    svg_image = get_contents(url)
    return Response(svg_image, mimetype='image/svg+xml')


# Route to generate and display the badge for followers
@app.route('/github/followers/')
def get_followers():
    username = request.args.get('username', '')
    params = {
        "label": "FOLLOW",
        "logo": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGZpbGw9IndoaXRlIiB2ZXJzaW9uPSIxLjEiIHdpZHRoPSIxNiIgaGVpZ2h0PSIxNiIgdmlld0JveD0iMCAwIDE2IDE2IiBjbGFzcz0ib2N0aWNvbiBvY3RpY29uLXBlcnNvbi1hZGQiIGFyaWEtaGlkZGVuPSJ0cnVlIj48cGF0aCBkPSJNNy45IDguNTQ4aC0uMDAxYTUuNTI4IDUuNTI4IDAgMCAxIDMuMSA0LjY1OS43NS43NSAwIDEgMS0xLjQ5OC4wODZBNC4wMSA0LjAxIDAgMCAwIDUuNSA5LjVhNC4wMSA0LjAxIDAgMCAwLTQuMDAxIDMuNzkzLjc1Ljc1IDAgMSAxLTEuNDk4LS4wODUgNS41MjcgNS41MjcgMCAwIDEgMy4xLTQuNjYgMy41IDMuNSAwIDEgMSA0Ljc5OSAwWk0xMy4yNSAwYS43NS43NSAwIDAgMSAuNzUuNzVWMmgxLjI1YS43NS43NSAwIDAgMSAwIDEuNUgxNHYxLjI1YS43NS43NSAwIDAgMS0xLjUgMFYzLjVoLTEuMjVhLjc1Ljc1IDAgMCAxIDAtMS41aDEuMjVWLjc1YS43NS43NSAwIDAgMSAuNzUtLjc1Wk01LjUgNGEyIDIgMCAxIDAtLjAwMSAzLjk5OUEyIDIgMCAwIDAgNS41IDRaIj48L3BhdGg+PC9zdmc+",
        "color": "236ad3",
        "style": "for-the-badge",
        "labelColor": "1155ba",
        "logoColor": "FFFFFF",
    }
    url = f"https://img.shields.io/github/followers/{username}?" + "&".join(
        f"{key}={value}" for key, value in params.items())
    svg_image = get_contents(url)
    return Response(svg_image, mimetype='image/svg+xml')


# Route to generate and display the badge for stars
@app.route('/github/stars/')
def get_stars():
    username = request.args.get('username', '')
    params = {
        "label": "STARS",
        "logo": "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIGZpbGw9IndoaXRlc21va2UiIHZlcnNpb249IjEuMSIgd2lkdGg9IjE2IiBoZWlnaHQ9IjE2IiB2aWV3Qm94PSIwIDAgMTYgMTYiIGNsYXNzPSJvY3RpY29uIG9jdGljb24tc3RhciIgYXJpYS1oaWRkZW49InRydWUiPjxwYXRoIGQ9Ik04IC4yNWEuNzUuNzUgMCAwIDEgLjY3My40MThsMS44ODIgMy44MTUgNC4yMS42MTJhLjc1Ljc1IDAgMCAxIC40MTYgMS4yNzlsLTMuMDQ2IDIuOTcuNzE5IDQuMTkyYS43NTEuNzUxIDAgMCAxLTEuMDg4Ljc5MUw4IDEyLjM0N2wtMy43NjYgMS45OGEuNzUuNzUgMCAwIDEtMS4wODgtLjc5bC43Mi00LjE5NEwuODE4IDYuMzc0YS43NS43NSAwIDAgMSAuNDE2LTEuMjhsNC4yMS0uNjExTDcuMzI3LjY2OEEuNzUuNzUgMCAwIDEgOCAuMjVabTAgMi40NDVMNi42MTUgNS41YS43NS43NSAwIDAgMS0uNTY0LjQxbC0zLjA5Ny40NSAyLjI0IDIuMTg0YS43NS43NSAwIDAgMSAuMjE2LjY2NGwtLjUyOCAzLjA4NCAyLjc2OS0xLjQ1NmEuNzUuNzUgMCAwIDEgLjY5OCAwbDIuNzcgMS40NTYtLjUzLTMuMDg0YS43NS43NSAwIDAgMSAuMjE2LS42NjRsMi4yNC0yLjE4My0zLjA5Ni0uNDVhLjc1Ljc1IDAgMCAxLS41NjQtLjQxTDggMi42OTRaIj48L3BhdGg+PC9zdmc+",
        "color": "55960c",
        "style": "for-the-badge",
        "labelColor": "488207",
        "logoColor": "FFFFFF",
    }
    url = f"https://img.shields.io/github/stars/{username}?" + "&".join(
        [f"{key}={value}" for key, value in params.items()])
    svg_image = get_contents(url)
    return Response(svg_image, mimetype='image/svg+xml')


if __name__ == '__main__':
    app.run(debug=True)
