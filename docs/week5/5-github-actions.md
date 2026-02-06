## 5. GitHub Actions for Continuous Integration (CI)

Continuous Integration (CI) is a DevOps software development practice where developers
frequently merge their code changes into a central repository. Each merge
triggers automated builds and tests to detect integration errors early, ensuring the codebase
remains stable.

Setting up a workflow was covered in COMP0035 and is not repeated. You can refer to
the [GitHub documentation](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python).

Go to Actions tab in GitHub Actions and you will see starter workflows. The Python Application
starter workflow is close to what you need so is a good starting point.

<img alt="GitHub Actions starter workflow" src="../../img/gha-workflow.png" width="250"/>

The GitHub actions environment includes chromedriver and Chrome. You don't need to explicitly
install them.

You may want to modify the GitHub Actions workflow `.yml` file in the following areas:

1. Modify the server operating system to match your computer if you are running Windows e.g. you can
   change `ubuntu-latest` to `windows-latest`
2. Modify the version of Python to match what you are using in the `name: Set up Python` section.
3. Include a step with `pip install –e .` in the `name: Install dependencies` section.
4. If not listed in `requirements.txt` or `pyproject.toml` then include a step to install
   `pip install playwright-pytest selenium pytest dash\[testing]` or any other test libraries you
   are using in
   the `name: Install dependencies` section
5. Read
   the [Playwright guidance](https://playwright.dev/python/docs/ci-intro#setting-up-github-actions)
   which explains where to add the `playwright install` step

[Next activity](6-further-info.md)