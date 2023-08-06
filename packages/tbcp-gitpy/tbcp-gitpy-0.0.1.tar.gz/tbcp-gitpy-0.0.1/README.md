<!--
Copyright (c) 2021 Bootcamp-Project contributors <contributors@bootcamp-project.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
-->
<a href="https://bootcamp-project.com/" target="_blank"><img src="https://bootcamp-project.com/tbcp.svg" align="right" height="200" /></a>

# The Bootcamp Project Companion

## DevOps Project Workflow CLI Tool

<img src="https://img.shields.io/badge/License-AGPL%20v.3-lightgrey?style=for-the-badge" />
<img src="https://img.shields.io/badge/Bootcamp-Project-blue?style=for-the-badge" />

## 🦄 About 🦄

**Minimum Viable Product**: *What is what we want?*

> *Build a CLI Tool to automate the boaring DevOps stuff*

- **What are the goals?**
  - [ ] **Work with Git Config**
  - [ ] **Work with Git Repositories**
    - [ ] Check if Git is installed
    - [ ] Check if CWD is a Git Repo
    - [X] Load Git Repo by Path
    - [X] Get Infos from Git Repo
    - [ ] Init new Git Repo
  - [ ] **Work with Git Files**
  - [ ] **Work with Git Commits**
  - [ ] **Work with Git Trees**
  - [ ] **Work with Git Tags**
    - [X] List Tags
    - [X] Create Tag
    - [ ] Delete Tag
  - [ ] **Work with Git Branches**
    - [X] List local branches of a repo
    - [ ] Create new local branch
      - [ ] optionally push to remote
    - [ ] Remove local branch
      - [ ] optionally remove from remote
    - [ ] Checkout specific branch
      - [ ] Checkout `main` branch
    - [ ] Rename `master` to `main`
  - [ ] **Work with Git Remotes**
  - [ ] **Work with Git Hooks**
  - [ ] **Work with Git Flows**

## 🚀 Getting Started 🚀

**Project Links**

- [Homepage][Project_Homepage]
- [Documentation][Project_Docs]
- [Repository][Repo_URL]
- [Issues][Repo_Issues]

### ✋ Prerequisites ✋

### 💪 Installation 💪

```bash
python3 setup.py install
```

### 😏 Development 😏

```bash
python3 setup.py develop
```

```bash
alias companion='/usr/local/bin/companion/'
```

### 🤓 Linting 🤓

### 🧐 Testing 🧐

### 🤩 Building 🤩

### 🥳 Publishing 🥳

### 😅 Support 😅

*Don't be shy!* You are also welcome to open a [post in the issue registar][Repo_Issues] for simple questions.

## ⭐️ Features ⭐️

- [**Smoke** and **Unit-tested**][Repo_Tests] modules
- Security-first production-ready [**configurations**][TBCP_Configurations] by default
- Extensive [**documentation**][Project_Docs]

### 😎 Built With 😎

<table>
<tr>
<td><a href="https://click.palletsprojects.com" target="_blank"><img src="https://cdr.bootcamp-project.com/logos/programming/click.svg" alt="Click" width="200"/></a></td>
<td><a href="https://www.python.org/" target="_blank"><img src="https://cdr.bootcamp-project.com/logos/programming/python.svg" alt="Python" width="200"/></a></td>
<td><a href="https://bootcamp-project.com/" target="_blank"><img src="https://bootcamp-project.com/tbcp.svg" alt="tbcp" width="200"/></a></td>
</tr>
</table>

### 🏆 Acknowledgements 🏆

Thanks for these awesome resources that were used during the development of the **Bootcamp: ESLint & Prettier Configuration**:

- Library: [Click][URL_Click]
- Library: [GitPython][URL_GitPython]
- How to: [RTFM.page - GitPython][RTFM_GitwithPython]

## 📑 Changelog 📑

See [CHANGELOG][Repo_Changelog] for more information.

## 📋 Roadmap 📋

- [ ] In the Initialization section
  - [ ] Create Nodejs and Python Projects
  - [ ] Automatic creation of Gitlab Projects
- [ ] Automate Versioning
  - [ ] in Python Projects
  - [ ] in Node.js Projects
    - [ ] with NPM
    - [ ] with Yarn
- [ ] Secret Management
- [ ] Log Messenger
- [ ] Parse Error messages and search on SE
  - [ ] Bash History

See the [open issues][Repo_Issues] for a list of proposed features (and known issues).

## 🤝 Contribute 🤝

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please read the [contribution guidelines][TBCP_Contribution] first.

0. [Give us a star][Repo_Stars], it's really important! 😅
1. Fork the Project: (`git clone https://gitlab.com/the-bootcamp-project/companion.git`)
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📜 License 📜

See [LICENSE][Repo_License] for more information.

## 💌 Contact 💌

[Bootcamp contributors][TBCP_Homepage] - `contributors` @ `bootcamp-project` .com

<!-- ---------------------------------------------------------------------------------------------------------------------------------- -->
<!-- ---------------------------------------------------------------------------------------------------------------------------------- -->
<!-- ---------------------------------------------------------------------------------------------------------------------------------- -->
[Project_Homepage]: https://companion.bootcamp-project.com
[Project_Docs]: https://companion.bootcamp-project.com
[Project_Install_Docs]: https://companion.bootcamp-project.com/#/install
[Project_Develop_Docs]: https://companion.bootcamp-project.com/#/develop
[Project_Linting_Docs]: https://companion.bootcamp-project.com/#/linting
[Project_esting_Docs]: https://companion.bootcamp-project.com/#/testing
[Project_Building_Docs]: https://companion.bootcamp-project.com/#/building
[Project_Publishing_Docs]: https://companion.bootcamp-project.com/#/publishing
<!-- ---------------------------------------------------------------------------------------------------------------------------------- -->
[Repo_URL]: https://gitlab.com/the-bootcamp-project/companion
[Repo_Issues]: https://gitlab.com/the-bootcamp-project/companion/-/issues
[Repo_Forks]: https://gitlab.com/the-bootcamp-project/companion/-/forks
[Repo_Stars]: https://gitlab.com/the-bootcamp-project/companion/-/starrers
[Repo_Tests]: https://gitlab.com/the-bootcamp-project/companion/-/tree/main/tests
[Repo_License]: https://gitlab.com/the-bootcamp-project/companion/-/blob/main/LICENSE
[Repo_Changelog]: https://gitlab.com/the-bootcamp-project/companion/-/blob/main/CHANGELOG
<!-- ---------------------------------------------------------------------------------------------------------------------------------- -->
[TBCP_Homepage]: https://bootcamp-project.com
[TBCP_Configurations]: https://configurations.bootcamp-project.com
[TBCP_Contribution]: https://bootcamp-project.com/#code_of_conduct
<!-- ---------------------------------------------------------------------------------------------------------------------------------- -->
[RTFM_GitwithPython]: https://dev.rtfm.page/#/working_with/git/interaction/with_python
<!-- ---------------------------------------------------------------------------------------------------------------------------------- -->
[URL_Python]: https://wiki.python.org/moin/BeginnersGuide/Download
[URL_Click]: https://click.palletsprojects.com
[URL_GitPython]: https://pypi.org/project/GitPython
<!-- ---------------------------------------------------------------------------------------------------------------------------------- -->
<!-- ---------------------------------------------------------------------------------------------------------------------------------- -->
<!-- ---------------------------------------------------------------------------------------------------------------------------------- -->
