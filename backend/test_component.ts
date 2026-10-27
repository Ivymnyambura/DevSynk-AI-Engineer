
import { getProjectName } from "./test_service";

export class ProjectComponent {
    displayProject(): string {
        return getProjectName();
    }
}
