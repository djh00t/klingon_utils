module.exports = {
  branches: [
    { name: "main" },
    { name: "release", prerelease: true }
  ],
  repositoryUrl: "https://github.com/djh00t/klingon_tools.git",
  plugins: [
    "@semantic-release/commit-analyzer",
    "@semantic-release/release-notes-generator",
    "@semantic-release/github",
    ["@semantic-release/git", {
      "assets": ["README.md", "pyproject.toml", "CHANGELOG.md"],
      "message": "chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}"
    }]
  ],
  preset: "conventionalcommits",
  releaseRules: [
    { type: "build", release: "patch" },
    { type: "chore", release: "patch" },
    { type: "ci", release: "patch" },
    { type: "docs", release: "patch" },
    { type: "feat", release: "minor" },
    { type: "fix", release: "patch" },
    { type: "perf", release: "patch" },
    { type: "refactor", release: "patch" },
    { type: "revert", release: "patch" },
    { type: "style", release: "patch" },
    { type: "test", release: "patch" },
    { type: "other", release: "patch" }
  ],
  parserOpts: {
    headerPattern: /^(?:[\u{1F300}-\u{1F6FF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]\s)?(\w*)(?:\((.*)\))?!?:\s(.*)$/u,
    headerCorrespondence: ['type', 'scope', 'subject'],
    noteKeywords: ["BREAKING CHANGE", "BREAKING CHANGES"]
  },
  writerOpts: {
    commitsSort: ["subject", "scope"]
  }
};
