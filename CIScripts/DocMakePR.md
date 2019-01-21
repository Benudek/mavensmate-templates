
## Install Github locally

Note, we assume you created a github account at this point and describe the process from there on.

Download Git for MAC e.g. Download Git for Mac at: https://git-scm.com/download/mac

on the command line check the version with 

> git —version

Now configure your user.name and user.email:g
> git config --global user.name "<full name>"
> git config --global user.email <email>

You can manually fork in the GitHub webUI or just run the script (https://github.com/konecorp/mavensmate-templates/blob/master/CIScripts/CreateLocalFeatureBranch to fork following below instructions.

## Some global settings

Depending on other repos you might be using with git, you should set some global settings

Configure git

Set the git user name and email to yours for all repositories
> git config --global user.name "Ukko Snowland"
> git config --global user.email Usnowland@lightsummer.com

Make sure crlf is converted to lf when committing changed
NOTE: Dependent on your own configuration, you might want to apply changes to the specific repository only. Then use --local instead of --global.
>git config --global core.autocrlf input

Ignore any file permission changes
>git config --global core.filemode false

Initialize the local repository


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

### Step 1. Create your git hub repo

There is a smart [program](https://github.com/konecorp/mavensmate-templates/blob/master/CIScripts/CreateLocalFeatureBranch) that can do all the heavy lifting for you. Then you just need to do your work, commit changes and submit PR. To run it:

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





### Step 2. Write Your Code

This is where the magic happens.

Create new code, fix bugs - awesome.

During you code, comparing files from the sandbox downloaded with the git repo and refreshing your local branch are two important processes


#### How to Keep Your Feature Branch Up-to-date [NEEDS CHECK & TEST]

If you make a PR right after you made a fork of the original repository, the two repositories are aligned and you can easily create a PR. If time passes the original repository starts diverging from your fork, so when you work on your PRs you need to keep your master fork in sync with the original repository.

You can tell the state of your fork, by going to https://github.com/Ukko/SFDC-MAIN and seeing something like:

```
This branch is 331 commits behind fastai:master.
```

If you synced the `int` branch with the original repository and you have feature branches that you're still working on, now you want to update those. For example to update your previously existing branch `my-cool-feature`:

   ```
   git checkout int
   git pull
   git checkout my-cool-feature
   ```
### Step 3: Copy changes from your metadata to your local git

Your specific workflow will depend on your team and your personal preferences. One typical way of working is to use a code comparison tool to adjust the files in your repo. You first change files in your sandbox, then you download the metadata into a local folder. Then you will compare this metadata with the ones already existing in the gut hub repo you downloaded in the previous step. Use a toll like BeyoncCompare to compare files & folders and copy over the right snippets, particularly for large files like profiles.


### Step 4. Push Your Changes

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

### Step 5. Submit Your PR to merge your feature branch to the INT environment branch

Go to github and make a new Pull Request:

  [NEEDS REVIEW]Working with feature branches, our process will be to commit the feature branch to an environment branch, here the INT branch. After your feature is successfully tested, you as developers will take the feature branch and open a PR to the respective Release Branch (see Step 9). Note, the INT branch never gets merged as a whole to a Release Branch, this will allow moving through separate User Stories instead of merging an entire INT branch, where some features might not have passed the QA 
   
   Usually, if you go to https://github.com/Ukko/SFDC-MAIN github will notice that you committed to a new branch and will offer you to make a PR, so you don't need to figure out how to do it.

   If for any reason it's not working, go to https://github.com/Ukko/SFDC-MAIN/tree/new-feature-branch (replace `new-feature-branch` with the real branch name, and click `[Pull Request]` in the right upper corner.

   If you work on several unrelated PRs, make different directories for each one, ideally using the same directory name as the branch name, to simplify things.

### Step 6. Auto Test of Your PR [NEEDS REVISIT, after test script existing]

After you created your PR, a number of scripts will automatically run. All tests need to pass and you need to check this.

### Step 7. Review your PR

The INT and Staging branch require mandatory one review. You need to arrange within your team, who does that and when. You cannot deploy the change before that. It is part of the developer reponsibility to arrange the review.

### Step 8. Deploy Your PR

After the automated tests passed and your reviewer approves the change, the changes will deploy. During that deploy the same tests, that run during the Merge will re-run and there will be additional tests run from across the projects

### Step 9. Check for regression errors the next day

Albeit we have 2 test stages, not all relevant tests for your code will have run. Your code might cause regression errors and specifically cause 101 SOQL errors in test scripts. For larg, riskful changes it is good practice to reach out to the Release Manager to check, in any case be prepared to lend a hand if the nightly regression tests report issue the next morning.

### Step 10. Merge your feature branch to a Release branch

  After your feature was successfully QAed by the test team, you will pick the feature branch and open a PR to the respective Release Branch. [THIS NEEDS CHECKING] When opening, automated test scripts will run again. A review will be enforced, this time this a review from the Release Manager however.

## More Tips & Tricks


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



Note: as an admin or if there are issues with your git commit, you will find additional commands in the Documentation: [ADJUST LINK] https://github.com/konecorp/SFDC-MAIN/pull/18709
