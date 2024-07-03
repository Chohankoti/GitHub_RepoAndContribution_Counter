from flask import Flask, request, jsonify
import requests
import re

app = Flask(__name__)

def get_contributions(username):
    url = f'https://github.com/users/{username}/contributions'
    response = requests.get(url)

    if response.status_code == 200:
        # Limit the HTML content to a reasonable snippet size
        snippet = response.text[:2000]  # Adjust the length as needed

        # Regular expression to match the contributions count (singular and plural)
        contributions_pattern = re.compile(
            r'<h2\s+class="f4\s+text-normal\s+mb-2">\s*(\d+)\s*contribution[s]?\s*in\s*the\s*last\s*year\s*</h2>',
            re.IGNORECASE | re.DOTALL
        )
        match = contributions_pattern.search(snippet)

        if match:
            contributions = match.group(1)
            return int(contributions)
        else:
            return "Unable to find contributions count."
    else:
        return f"Error: {response.status_code}"

def get_repo_count(username):
    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)

    if response.status_code == 200:
        repos = response.json()
        return len(repos)
    else:
        return f"Error: {response.status_code}"

@app.route('/profiles', methods=['POST'])
def profiles():
    data = request.json
    if not isinstance(data, list):
        return jsonify({"error": "Input should be a JSON array of objects containing username, email, and id."}), 400

    results = []
    for item in data:
        username = item.get('username')
        email = item.get('email')
        user_id = item.get('id')
        
        if not username or not email or not user_id:
            results.append({"error": "Each object must contain 'username', 'email', and 'id'."})
            continue

        contributions = get_contributions(username)
        repo_count = get_repo_count(username)

        if isinstance(contributions, int) and isinstance(repo_count, int):
            results.append({
                "id": user_id,
                "username": username,
                "email": email,
                "contributions": contributions,
                "repositories": repo_count
            })
        else:
            results.append({
                "id": user_id,
                "username": username,
                "email": email,
                "error": contributions if isinstance(contributions, str) else repo_count
            })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)







# from flask import Flask, request, jsonify
# import requests
# import re

# app = Flask(__name__)

# def get_contributions(username):
#     url = f'https://github.com/users/{username}/contributions'
#     response = requests.get(url)

#     if response.status_code == 200:
#         # Limit the HTML content to a reasonable snippet size
#         snippet = response.text[:182][80:]  # Adjust the length as needed

#         # Regular expression to match the contributions count
#         contributions_pattern = re.compile(
#             r'<h2\s+class="f4\s+text-normal\s+mb-2">\s*(\d+)\s*contributions\s*in\s*the\s*last\s*year\s*</h2>',
#             re.IGNORECASE | re.DOTALL
#         )
#         match = contributions_pattern.search(snippet)

#         if match:
#             contributions = match.group(1)
#             return int(contributions)
#         else:
#             return "Unable to find contributions count."
#     else:
#         return f"Error: {response.status_code}"

# def get_repo_count(username):
#     url = f'https://api.github.com/users/{username}/repos'
#     response = requests.get(url)

#     if response.status_code == 200:
#         repos = response.json()
#         return len(repos)
#     else:
#         return f"Error: {response.status_code}"

# @app.route('/profile', methods=['GET'])
# def profile():
#     username = request.args.get('username')
#     if not username:
#         return jsonify({"error": "Username parameter is required."}), 400

#     contributions = get_contributions(username)
#     repo_count = get_repo_count(username)

#     if isinstance(contributions, int) and isinstance(repo_count, int):
#         return jsonify({
#             "username": username,
#             "contributions": contributions,
#             "repositories": repo_count
#         })
#     else:
#         return jsonify({
#             "error": contributions if isinstance(contributions, str) else repo_count
#         }), 404

# if __name__ == '__main__':
#     app.run(debug=True)
