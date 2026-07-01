const repository = process.env.RENOVATE_REPOSITORY || process.env.GITHUB_REPOSITORY;

if (!repository) {
  throw new Error("RENOVATE_REPOSITORY or GITHUB_REPOSITORY must be set");
}

module.exports = {
  platform: "github",
  onboarding: false,
  requireConfig: "optional",
  repositories: [repository],

  branchPrefix: "renovate-dhi/",
  dependencyDashboard: true,
  enabledManagers: ["dockerfile"],
  labels: ["dependencies", "renovate", "dhi"],

  ignorePaths: [
    "digest-refresh-test/consumer/**",
    "digest-refresh-test/fixture/**",
  ],

  hostRules: [
    {
      hostType: "docker",
      matchHost: "dhi.io",
      username: process.env.DHI_USERNAME,
      password: process.env.DHI_TOKEN,
    },
  ],

  packageRules: [
    {
      description: "DHI nginx digest-only test: disable visible tag bumps",
      matchManagers: ["dockerfile"],
      matchDatasources: ["docker"],
      matchPackageNames: ["dhi.io/nginx", "nginx"],
      matchUpdateTypes: ["major", "minor", "patch"],
      enabled: false,
    },
    {
      description: "Group DHI nginx digest refreshes",
      matchManagers: ["dockerfile"],
      matchDatasources: ["docker"],
      matchPackageNames: ["dhi.io/nginx", "nginx"],
      matchUpdateTypes: ["digest"],
      groupName: "DHI nginx digest refresh",
    },
  ],
};
