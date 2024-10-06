cd "$(dirname "$0")"
current_directory=$(pwd)
echo "Current directory is: $current_directory"
cd client
npm install
npm run serve