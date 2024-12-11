// store/project.ts
import { defineStore } from 'pinia';

export const useProjectStore = defineStore('project', {
    state: () => ({
        project_id: null,
        project_name: null,
        project_description: null,
    }),
    actions: {
        setProject(project) {
            this.project_id = project.project_id;
            this.project_name = project.project_name;
            this.project_description = project.project_description;
        },
        clearProject() {
            this.project_id = null;
            this.project_name = null;
            this.project_description = null;
        },
    },
});
