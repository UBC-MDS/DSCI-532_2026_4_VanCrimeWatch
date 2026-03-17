# Contributing to VanCrimeWatch

Contributions of all kinds are welcome for the VanCrimeWatch and are greatly appreciated!
Every little bit helps, and credit will always be given.

## Branching and Workflow

This project follows a Github Flow Workflow.

- The main branch always contains stable, production-ready code
- Direct commits to the 'main' branch are prohibited.
- All work should be based off and merged into the `dev` branch via pull request.
- Branches should be named with appropriate prefixes: `feat-` or `fix-`.
- Each pull request must be reviewed and approved by at least one other team member before merging.

## Pull Request Discipline

Keep PRs focused and reviewable:

- Each PR should address a **single, specific problem or feature**. 
- Avoid large PRs and keep line count changes small and scoped. Larger fixes can be broken into smaller PRs to make testing and review smoother.
- New features **must** include:
  - A small update to the relevant **specification** in `reports/`
  - Updated and documented **Tests** (if applicable)
- For significant UI changes, include a Posit Cloud preview link in the PR description to speed up review.

## Analysis and Testing

- Exploratory analysis and notebook-based testing should be placed in `reports/` as Jupyter notebooks.
- Unit tests (Pytest) live in `tests/` and should cover core data-filtering logic.
- UI tests use Playwright. Run the full suite with:

```bash
conda activate vancrimewatch
playwright install
pytest tests/
```

## LLM / AI Features

The AI Explorer tab uses the Anthropic API and incurs token costs and retrieves LLM outputs. When contributing to AI-related features:

- **Caution of use of LLMs** -  Please be mindful of unpredictable LLM behaviour
- **Do not log or expose sensitive user queries.** Be mindful of what gets sent to the API. Take care that the database is correctly set up with appropriate security.
- Test AI-related changes locally using your own `.env` API key (see setup below). Do not commit API keys.

## Types of Contributions

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

## Proposing New Features

Before implementing new features, open an issue on GitHub to propose it first. A good feature proposal should include:

- **What** — a clear description of the feature and the problem it solves
- **Why** — how it fits the dashboard's purpose (helping business owners assess Vancouver crime risk)
- **Scope** — a rough sense of what files/components will be touched
- **Alternatives considered** — any other approaches you evaluated

Wait for maintainer feedback before opening a PR. This helps avoid clashes and duplicate work and keeps the project focused.

### Write Documentation

VanCrimeWatch could always use more documentation, whether as
part of the official documentation, in docstrings, or even on the web in blog
posts, articles, and such. Just
[open an issue](https://github.com/UBC-MDS/DSCI_532_2026_4_VanCrimeWatch/issues)
to let us know what you will be working on so that we can provide you with guidance.

## Writing Tests

If new edge cases are found, users can contribute new tests for the project. Tests live in `tests/`. There are two types:

- **Logic (Unit) tests (Pytest)** — cover core data-filtering and business logic in `src/`
- **UI tests (Playwright)** — cover dashboard interactions and component rendering

When writing tests:

- Each test should target a single, specific behaviour
- Use descriptive test names that explain what is being verified (e.g. `test_filter_empty_years`)
- If your change touches filtering logic, a unit test is expected
- If your change touches a UI component, consider adding or updating a Playwright test

Run the full suite before opening a PR:
```bash
conda activate vancrimewatch
playwright install  # only needed once
pytest tests/
```

### Submit Feedback

The best way to send feedback is to file an issue at
https://github.com/UBC-MDS/DSCI_532_2026_4_VanCrimeWatch/issues. If your feedback fits the format of one of
the issue templates, please use that. Remember that this is a volunteer-driven
project and everybody has limited time.

## Get Started

Fork and clone the repository:

```bash
git clone git@github.com:your_github_username/DSCI_532_2026_4_VanCrimeWatch.git
cd DSCI_532_2026_4_VanCrimeWatch
```

### Setting Up the Environment

```bash
conda env create -f environment.yml
conda activate vancrimewatch
```

### Configure Environment Variables

Create a `.env` file in the project root:

```
ANTHROPIC_API_KEY=your_api_key_here
PYMONGO_URI=mongodb+srv://<user>:<pass>@cluster.mongodb.net/?appName=<cluster>
```

### Create a Branch

Branch off `dev`, use `fix` or `feat` as a prefix for your branch name.

```bash
git checkout dev
git checkout -b feat-name-of-your-feature
```

Now you can make your changes locally.

Commit your changes and push your branch to GitHub. Please use [semantic
   commit messages](https://www.conventionalcommits.org/).

```bash
git add .
git commit -m "feat: summarize your changes"
git push -u origin feat-name-of-your-feature
```

Then open a pull request **targeting `dev`**.

### Run the Dashboard Locally

```bash
shiny run src/app.py --reload
```

## Code of Conduct

VanCrimeWatch is released with a [Code of Conduct](https://github.com/UBC-MDS/DSCI_532_2026_4_VanCrimeWatch/blob/main/CODE_OF_CONDUCT.md). By contributing, you agree to abide by its terms.

## Attribution and Code of Conduct

The following was attributed from [AI_bias_in_farming](https://github.com/skysheng7/AI_bias_in_farming/blob/main/CONTRIBUTING.md). Please note that the VanCrimeWatch Dashboard is released with a [Code of Conduct](https://github.com/UBC-MDS/DSCI_532_2026_4_VanCrimeWatch/blob/main/CODE_OF_CONDUCT.md). By contributing to this project you agree to abide by its terms.