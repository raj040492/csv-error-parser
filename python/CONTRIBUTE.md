We strongly believe that no matter how much time we spent in writing bug detecting codes, there is always that 1% of bugs which keeps eluding us. Only with your support will we able to conquer that part.

Please take a moment to review this document in order to make the contribution process easy and effective for everyone involved.

Before contributing towards this tool, we recommend you to use this tool with any random .csv file so as to realize its full potential and limitations(which is where you will step in).

	#Clone this repo into your workstation
	git clone https://github.com/raj040492/CSV-anamoly-detector.git 

	Follow README.md for few basic steps which will run you through the tool.


Suggestions to improve the tool (when you are hard pressed for time to write the code) is also welcome.


<h2> Submit Issues </h2>

We are only human and To err is human. Thus there is a chance that there might be a loophole in our code that we missed. You can always contribute to our tool by submitting issues.

Creating/Submitting issues has never been so easier.

Use this handy <a href= "https://help.github.com/articles/creating-an-issue/" target="_blank">link</a> when in doubt

<h2>Pull requests</h2>

Good pull requests are a fantastic help as long as they remain within the ambit of the tool's scope.

The following steps if followed would be highly appreciated :

1) Fork the repo, Clone the fork

	# Clone your fork of the repo into the current directory
	git clone https://github.com/<your-username>/CSV-anamoly-detector.git
	# Assign the original repo to a remote called "upstream"
	git remote add upstream https://github.com/h5bp/CSV-anamoly-detector.git

2) If you cloned a long back pull the latest from the master:

	git checkout master
	git pull upstream master


3) Please make your commits in tiny chunks rather than one goliathic commit.
   
   Kindly name the commits in such a way that even a layman could make sense out of it.


4) Create a new branch where you can push your own changes/upgrades.

	git checkout -b <topic-branch-name>

5) Locally merge (or rebase) the upstream development branch into your topic branch:

	git pull [--rebase] upstream master

6) Push your topic branch up to your fork:

	git push origin <topic-branch-name>

7) <a href= "https://help.github.com/articles/using-pull-requests/" target="_blank">Open a Pull Request </a> with a clear title and description.