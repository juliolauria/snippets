# As seen on https://medium.com/analytics-vidhya/folder-structure-for-machine-learning-projects-a7e451a8caaa

# Install cookie cutter
!pip install cookiecutter

# Create a folder for the project and run the following:
cookiecutter -c v1 https://github.com/drivendata/cookiecutter-data-science

# Add folder to Git:
cd my-test
# Initialize the git
git init
# Add all the files and folder
git add .
# Commit the files
git commit -m "Initialized the repo with cookiecutter data science structure"
# Set the remote repo URL
git remote add origin https://github.com/your_user_id/my-test.git
git remote -v
# Push to changes from local repo to github
git push origin master
