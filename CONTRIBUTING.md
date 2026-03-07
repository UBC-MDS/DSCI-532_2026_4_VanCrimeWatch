# Contributing to VanCrimeWatch

Contributions of all kinds are welcome for the VanCrimeWatch and are greatly appreciated!
Every little bit helps, and credit will always be given.

## Branching and Workflow

This project follows a Github Flow Workflow.

- The main branch always contains stable, production-ready code
- Direct commits to the 'main' branch are prohibited.
- All work should be conducted on short-lived branches created from 'main'.
- Branches should be named using appropriate prefixes such as 'feat-' or 'fix-'.
- Changes must be proposed via pull request to the main branch.
- Each Pull request must be reviewed by at least one other team member and granted approval before merging. 

## Example Contributions

You can contribute in many ways, for example:

* [Report bugs](#report-bugs)
* [Fix Bugs](#fix-bugs)
* [Implement Features](#implement-features)
* [Write Documentation](#write-documentation)
* [Submit Feedback](#submit-feedback)

### Report Bugs

Report bugs at https://github.com/UBC-MDS/DSCI_532_2026_4_VanCrimeWatch/issues.

**If you are reporting a bug, please follow the template guidelines. The more
detailed your report, the easier and thus faster we can help you.**

### Fix Bugs

Look through the GitHub issues for bugs. Anything labelled with `bug` and
`help wanted` is open to whoever wants to implement it. When you decide to work on such
an issue, please assign yourself to it and add a comment that you'll be working on that,
too. If you see another issue without the `help wanted` label, just post a comment, the
maintainers are usually happy for any support that they can get.

### Implement Features

Look through the GitHub issues for features. Anything labelled with
`enhancement` and `help wanted` is open to whoever wants to implement it. As
for [fixing bugs](#fix-bugs), please assign yourself to the issue and add a comment that
you'll be working on that, too. If another enhancement catches your fancy, but it
doesn't have the `help wanted` label, just post a comment, the maintainers are usually
happy for any support that they can get.

### Write Documentation

VanCrimeWatch could always use more documentation, whether as
part of the official documentation, in docstrings, or even on the web in blog
posts, articles, and such. Just
[open an issue](https://github.com/UBC-MDS/DSCI_532_2026_4_VanCrimeWatch/issues)
to let us know what you will be working on so that we can provide you with guidance.

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/UBC-MDS/DSCI_532_2026_4_VanCrimeWatch/issues. If your feedback fits the format of one of
the issue templates, please use that. Remember that this is a volunteer-driven
project and everybody has limited time.

## Get Started

To make changes to our dashboard, first fork and then clone the repository:

```shell
git clone git@github.com:your_github_username/DSCI_532_2026_4_VanCrimeWatch.git
cd DSCI_532_2026_4_VanCrimeWatch
```

### Setting Up the Environment

```bash
conda env create -f environment.yml
conda activate vancrimewatch
```

### Create a New Branch

Create a branch for local development using the default branch (typically `main`) as a starting point. Use `fix` or `feat` as a prefix for your branch name.

```shell
git checkout main
git checkout -b fix-name-of-your-bugfix
```

Now you can make your changes locally.

Commit your changes and push your branch to GitHub. Please use [semantic
   commit messages](https://www.conventionalcommits.org/).

```shell
git add .
git commit -m "fix: summarize your changes"
git push -u origin fix-name-of-your-bugfix
```

Open the link displayed in the message when pushing your new branch in order
to submit a pull request.

### Running the Dashboard Locally

```bash
cd DSCI_532_2026_4_VanCrimeWatch
conda activate vancrimewatch

shiny run src/app.py --reload
```

## Attribution and Code of Conduct

The following was attributed from [AI_bias_in_farming](https://github.com/skysheng7/AI_bias_in_farming/blob/main/CONTRIBUTING.md). Please note that the VanCrimeWatch Dashboard is released with a [Code of Conduct](https://github.com/UBC-MDS/DSCI_532_2026_4_VanCrimeWatch/blob/main/CODE_OF_CONDUCT.md). By contributing to this project you agree to abide by its terms.