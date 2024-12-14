import { defineStore } from 'pinia';

export const useProjectStore = defineStore('project', {
    state: () => ({
        project_id: null as number | null,
        project_name: null as string | null,
        project_description: null as string | null,
        projects: [] as Array<{
            project_id: number;
            project_name: string;
            project_description: string | null;
        }>,
    }),
    actions: {
        setProject(project: { project_id: number; project_name: string; project_description: string | null }) {
            this.project_id = project.project_id;
            this.project_name = project.project_name;
            this.project_description = project.project_description;
        },
        clearProject() {
            this.project_id = null;
            this.project_name = null;
            this.project_description = null;
        },
        setProjects(projects: Array<{ project_id: number; project_name: string; project_description: string | null }>) {
            this.projects = projects;
        },
        updateProjectState(updatedProject: { project_id: number; project_name: string; project_description: string | null }) {
            const index = this.projects.findIndex((p) => p.project_id === updatedProject.project_id);
            if (index !== -1) {
                this.projects[index] = updatedProject;
            }
        },
    },
});
