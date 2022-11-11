## 🚧 🛰️ Overview 🚧

Write an explanation of the PR goal here.  Remove the caution emoji when the PR is no longer a draft PR.

## ✨ Change Description/Rationale

- ➕ Add the commit message descriptions here.  Much of this can be taken from the Issue being addressed.

If longer explanation is required, it goes in paragraphs below the title sentence.  Please keep these in sync with the commit messages.

## 🧪 Test Coverage

Paste the coverage output for the relevant files below, and delete this line.  This output comes from running ``tox``.

```
---------- coverage: platform darwin, python 3.7.12-final-0 ----------
Name                                             Stmts   Miss Branch BrPart     Cover   Missing
-----------------------------------------------------------------------------------------------
src/groundstation/excepthook.py                     92      8     24      1    92.24%   46-50
```
- **45-60:** Add an explanation bullet point to explain why there are coverage gaps

## 🚨 Quality Deviations

If there are commits that do not fully conform to the ``pre-commit`` hook checks, explain why here.  Common explanations may involve deprecated code or files that are being updated to use the main PR code but are not being directly addressed otherwise.

## 👀 Reviewer Checklist
- [ ] List of steps that a reviewer should follow to ensure changes are working
- [ ] Any tests that should be run by the reviewer and what they should look for in the output

## ✅ PR Checklist

(These are not all checked by the submitter, only check the items that are _actually_ complete)

- [ ] Remove or update the PR template boilerplate text
- [ ] Reviewers Requested
- [ ] Labels added
- [ ] Projects associated
- [ ] Milestone assigned
- [ ] All docstrings are formatted as google docstrings with filled out types and explanations; Any code that was edited and contains a prose description of the functional execution, and preferably a ``doctest`` compatible example
- [ ] Docstring examples are all ``doctest`` compliant
- [ ] Any file or folder names are manipulated via ``pathlib.Path``
- [ ] Non-public imports and API elements are prefixed with a single underscore or the package ``__all__`` variable is set
- [ ] All ``noqa`` statements for skipping lint rules are justified
- [ ] Commits mention issue and/or PR numbers at the bottom of the message with the [Username/Repository#](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/autolinked-references-and-urls) format
- [ ] Relevant issues are linked into the PR (issues mentioned in overview should link for you)
- [ ] TODOs are completed
- [ ] Reviewer checklist is updated

## 🚀 TODOs

- [x] This is a list of TODOs that are relevant to this PR
- [ ] Add items to this list that shouldn't be forgotten, or that reviewers have requested that you complete.

## 📌 Future Work

- Use this section to document the related work that you *are not* doing.
- Documenting Future Work and explanations therof will help reviewers understand why those things are not being done in this PR.
