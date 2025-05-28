# 📄 Tenders Management System - Frontend

A React-based frontend application for displaying and managing tender information with a clean, modern UI.

## 🚀 Features

- ✅ Tender listing with pagination  
- ✅ Responsive design  
- ✅ Customizable items per page  
- ✅ Clean and modern UI  

---

## 📦 Prerequisites

Before getting started, ensure you have the following installed:

- [Node.js](https://nodejs.org/) (v14 or higher)  
- [npm](https://www.npmjs.com/) (v6 or higher) or [Yarn](https://yarnpkg.com/)  
- [Git](https://git-scm.com/) (optional)

---

## 🛠️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/tenders-frontend.git
cd tenders-frontend
Install dependencies:

Using npm:

bash
Copy
Edit
npm install
Or using yarn:

bash
Copy
Edit
yarn install
⚙️ Configuration
Create a .env file in the root directory:

bash
Copy
Edit
touch .env
Add the following environment variable:

env
Copy
Edit
VITE_API_BASE_URL=http://13.213.35.77:5000
# For development with proxy:
# VITE_API_BASE_URL=/api
📜 Available Scripts
In the project directory, you can run:

🧪 Development
bash
Copy
Edit
npm run dev
# or
yarn dev
Runs the app in development mode.
Visit http://localhost:5173 to view it in your browser.

🛠 Production Build
bash
Copy
Edit
npm run build
# or
yarn build
Builds the app for production into the dist folder.
Includes optimizations such as minification and hashed filenames.

🔍 Preview Production Build
bash
Copy
Edit
npm run preview
# or
yarn preview
Locally previews the production build.

🔌 Backend API Requirements
The frontend expects the backend API to:

Have CORS enabled or use a proxy in development.

Provide the following endpoint:

POST /post-page
Returns paginated tender data.

Example request body:

json
Copy
Edit
{
  "page": 1,
  "limit": 5
}
🧰 Troubleshooting
❌ CORS Issues
If you encounter CORS errors during development:

✅ Recommended:
Enable CORS in the backend server.

🔁 Alternative: Use Vite proxy
Update vite.config.js:

javascript
Copy
Edit
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://13.213.35.77:5000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    }
  }
});
Then, prefix your API calls with /api.

🚢 Deployment
For deployment instructions, refer to the DEPLOYMENT.md file (if available).

🤝 Contributing
Pull requests are welcome!
For major changes, please open an issue first to discuss what you'd like to change.

📄 License
This project is licensed under the MIT License.

yaml
Copy
Edit

---

Let me know if you'd like me to add badges (build status, license, version, etc.), contribution guidelines, or an example API response display.







