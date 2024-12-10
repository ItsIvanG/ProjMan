import { defineStore } from 'pinia';

export const useProjectStore = defineStore('project', {
  state: () => ({
    projects: [], // All projects
    selectedProject: null, // The selected project's data
  }),
  actions: {
    setProjects(projects) {
      this.projects = projects;
    },
    setSelectedProject(project) {
      this.selectedProject = project;
    },
  },
});
