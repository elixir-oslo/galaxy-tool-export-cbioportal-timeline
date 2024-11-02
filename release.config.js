module.exports = {
  branches: ['main'],
  plugins: [
    '@semantic-release/commit-analyzer',
    [
      '@semantic-release/release-notes-generator',
      {
        preset: 'conventionalcommits',
        presetConfig: {
          types: [
            { type: 'feat', section: 'Features' },
            { type: 'fix', section: 'Bug Fixes' },
            { type: 'chore', section: 'Chores', hidden: true },
            { type: 'docs', section: 'Documentation' },
            { type: 'style', section: 'Styles', hidden: true },
            { type: 'refactor', section: 'Code Refactoring' },
            { type: 'perf', section: 'Performance Improvements' },
            { type: 'test', section: 'Tests', hidden: true }
          ]
        }
      }
    ],
    '@semantic-release/changelog',
    '@semantic-release/github',
    '@semantic-release/git'
  ]
};