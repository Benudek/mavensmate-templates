
## Install Github locally

Note, we assume you created a github account at this point and describe the process from there on.

Download Git for MAC e.g. Download Git for Mac at: https://git-scm.com/download/mac

on the command line check the version with 

> git —version

Now configure your user.name and user.email:g
> git config --global user.name "<full name>"
> git config --global user.email <email>

You can manually fork in the GitHub webUI or just run the script (ADJUST https://github.com/konecorp/SFDC-MAIN/pull/18710/commits/18512f36194c9e057fc6893c6ab87ebd2f8afbaa) to fork.	


## How to Make a Pull Request (PR)

While this guide is mostly suitable for creating PRs for any github project, it includes steps specific to the `KONE` project repositories. 

Focus is exlaining how use the Automation scripts

The following instructions use `USERNAME` as a github username placeholder. The easiest way to follow this guide is to copy-n-paste the whole section into a file, replace `USERNAME` with your real username and then follow the steps.

The following url shows username, repository and code module, in the order they appear in the URL:

```
https://github.com/Ukko/SFDC-MAIN/tree/master/awesomecode
                     |       |                  |
                 username reponame        modulename
```

### Automation

There is a smart [program](ADJUST https://github.com/konecorp/SFDC-MAIN/pull/18710/commits/18512f36194c9e057fc6893c6ab87ebd2f8afbaa) that can do all the heavy lifting for you. Then you just need to do your work, commit changes and submit PR. To run it:

```
Copy the script KONE-make-pr-branch to your local machine
Ensure you have curl and Github (...) installed
## curl -O https://raw.githubusercontent.com/INSERTURL
chmod a+x fastai-make-pr-branch
./KONE-make-pr-branch https Ukko SFDC-MAIN awesome-feature
```

For more details run:
```
./KONE-make-pr-branch
```



#### Subsequent times

If you make a PR right after you made a fork of the original repository, the two repositories are aligned and you can easily create a PR. If time passes the original repository starts diverging from your fork, so when you work on your PRs you need to keep your master fork in sync with the original repository.

You can tell the state of your fork, by going to https://github.com/Ukko/SFDC-MAIN and seeing something like:

```
This branch is 331 commits behind fastai:master.
```

So, let's synchronize the two: [THIS SECTION NEEDS TO TEST AND ADJUSTMENT]

1. Place yourself in the `master` branch of the forked repository, which should be your baseline. Typically that is INT, on other occasions that could be staging:

   * Either you go back to a repository you checked out earlier and switch to the `master` branch:

   ```
   cd KONE-fork
   git checkout master
   ```

   * or you make a new clone

   ```
   git clone git://github.com/Ukko/SFDC-MAIN.git KONE-fork
   cd KONE-fork
   git remote add upstream git@github.com:konecorp/SFDC-MAIN.git
   ```

     ```
     
   Use the https version https://github.com/Ukko/SFDC-MAIN if you don't have ssh configured with github.

2. Sync the forked repository with the original repository:

   ```
   git fetch upstream
   git checkout master
   git merge --no-edit upstream/int
   git push
   ```

   Now you can branch off this synced `int` branch.

   Validate that your fork is in sync with the original repository by going to https://github.com/Ukko/SFDC-MAIN and checking that it says:

   ```
   This branch is even with fastai:int.
   ```
   Now you can work on a new PR.


### Step 2. Write Your Code

This is where the magic happens.

Create new code, fix bugs - awesome.

### Step 3. Push Your Changes

1. When you're happy with the results, commit the new code:

   ```
   git commit -m"#12345 commit message for awesome code"
   ```
   where 12345 is the targy number of your task. With the # targy can identify the change and show it in the code section

   If you created new files, first tell git to track them:

   ```
   git add newfile1 newdir2 ...
   ```
   and then commit.

2. Finally, push the changes into the branch of your fork:

   ```
   git push
   ```

### Step 4. Submit Your PR to merge your feature branch to the INT environment branch

Go to github and make a new Pull Request:

  [NEEDS REVIEW]Working with feature branches, our process will be to commit the feature branch to an environment branch, here the INT branch. After your feature is successfully tested, you as developers will take the feature branch and open a PR to the respective Release Branch (see Step 9). Note, the INT branch never gets merged as a whole to a Release Branch, this will allow moving through separate User Stories instead of merging an entire INT branch, where some features might not have passed the QA 
   
   Usually, if you go to https://github.com/Ukko/SFDC-MAIN github will notice that you committed to a new branch and will offer you to make a PR, so you don't need to figure out how to do it.

   If for any reason it's not working, go to https://github.com/Ukko/SFDC-MAIN/tree/new-feature-branch (replace `new-feature-branch` with the real branch name, and click `[Pull Request]` in the right upper corner.

   If you work on several unrelated PRs, make different directories for each one, ideally using the same directory name as the branch name, to simplify things.

### Step 5. Auto Test of Your PR [NEEDS REVISIT, after test script existing]

After you created your PR, a number of scripts will automatically run. All tests need to pass and you need to check this.

### Step 6. Review your PR

The INT and Staging branch require mandatory one review. You need to arrange within your team, who does that and when. You cannot deploy the change before that. It is part of the developer reponsibility to arrange the review.

### Step 7. Deploy Your PR

After the automated tests passed and your reviewer approves the change, the changes will deploy. During that deploy the same tests, that run during the Merge will re-run and there will be additional tests run from across the projects

## Step 8. Check for regression errors the next day

Albeit we have 2 test stages, not all relevant tests for your code will have run. Your code might cause regression errors and specifically cause 101 SOQL errors in test scripts. For larg, riskful changes it is good practice to reach out to the Release Manager to check, in any case be prepared to lend a hand if the nightly regression tests report issue the next morning.

## Step 9. Merge your feature branch to a Release branch

  After your feature was successfully QAed by the test team, you will pick the feature branch and open a PR to the respective Release Branch. [THIS NEEDS CHECKING] When opening, automated test scripts will run again. A review will be enforced, this time this a review from the Release Manager however.

## More Tips & Tricks

### How to Keep Your Feature Branch Up-to-date [NEEDS CHECK & TEST]

If you synced the `int` branch with the original repository and you have feature branches that you're still working on, now you want to update those. For example to update your previously existing branch `my-cool-feature`:

   ```
   git checkout int
   git pull
   git checkout my-cool-feature
   ```

### Where am I? [NEEDS TEST]


* Which repository am I in?

   ```
   git config --get remote.origin.url | sed 's|^.*//||; s/.*@//; s/[^:/]\+[:/]//; s/.git$//'
   ```
   e.g.: `Ukko/SFDC-MAIN`

* Which branch am I on?

   ```
   git branch | sed -n '/\* /s///p'
   ```
   e.g.: `new-feature-branch7`

* Combined:

   ```
   echo $(git config --get remote.origin.url | sed 's|^.*//||; s/.*@//; s/[^:/]\+[:/]//; s/.git$//')/$(git branch | sed -n '/\* /s///p')
   ```
   e.g.: `Ukko/SFDC-MAIN/new-feature-branch7`

But that's not a very efficient process to constantly ask the system to tell you where you are. Why not make it automatic and integrate this into your bash prompt (assuming that use bash).

#### bash-git-prompt  [NEEDS TEST]

Enter [`bash-git-prompt`](https://github.com/magicmonty/bash-git-prompt), which not only tells you which virtual environment you are in and which `username`, `repo`, `branch` you're on, but it also provides very useful visual indications on the state of your git checkout - how many files have changed, how many commits are waiting to be pushed, whether there are any upstream changes, and much more.

[EXAMPLE]


## hub  [NEEDS TEST]

hub == hub helps you win at git

[`hub`](https://github.com/github/hub) is the command line GitHub. It provides integration between git and github in command line. One of the most useful commands is creating pull request by just typing `hub pull-request` in your terminal.

Installation:

There is a variety of [ways to install](https://github.com/github/hub#installation) this application (written in go), but the easiest is to download the latest binary for your platform at https://github.com/github/hub/releases/latest, un-archiving the package and running `./install`, for example for the `linux-64` build:

```
wget https://github.com/github/hub/releases/download/v2.5.1/hub-linux-amd64-2.5.1.tgz
tar -xvzf hub-linux-amd64-2.5.1.tgz
cd hub-linux-amd64-2.5.1
sudo ./install
```

You can add a prefix to install it to a different location, for example, under your home:

```
prefix=~ ./install
```


```
curl https://api.github.com/repos/github/hub/releases/latest
```
identifying user's platform, retrieving the corresponding to that platform package, unarchiving it, identifying the conda base as shown above, and running `install` with that prefix. If you work on it, please write it in python, so that windows users w/o bash could use it too. It'd go into `tools/hub-install` in the `fastai` repo.


Note: as an admin or if there are issues with your git commit, you will find additional commands in the Documentation: [ADJUST LINK] https://github.com/konecorp/SFDC-MAIN/pull/18709
