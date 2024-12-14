import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useProjectListStore = defineStore('projectListStore', () => {
  // State: List of projects
  const projects = ref([]);
  const selectedProject = ref(null);

  // Action: Set projects list
  const setProjects = (newProjects) => {
    projects.value = newProjects;
  };

  // Action: Add a single project to the list
  const addProject = (project) => {
    projects.value.push(project);
  };

  // Action: Set the selected project
  const setSelectedProject = (project) => {
    selectedProject.value = project;
  };

  const clearSelectedProject = (project) => {
    selectedProject.value = null;
  };

  return {
    projects,
    selectedProject,
    setProjects,
    addProject,
    setSelectedProject,
    clearSelectedProject
  };
});
