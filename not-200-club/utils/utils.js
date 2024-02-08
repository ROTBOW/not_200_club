/**
 * The function `getNames` takes in a data object and returns a set of unique names from the object.
 * @param data - An object containing coaches as keys and an array of seekers as values. Each seeker is
 * represented as a string.
 * @returns a Set containing all the names of the seekers in the given data.
 */
export const getNames = (data) => {
    let res = new Set();

    for (let coach in data) {
        let seekers = data[coach];
        for (let seeker in seekers) {
            res.add(seeker.toLowerCase());
        }
    }


    return res;
}

/**
 * The function `parseIssues` takes an array of issues and returns a modified version of the array
 * based on certain conditions.
 * @param issues - The `issues` parameter is an array that contains a list of issues.
 * @returns the parsed issues.
 */
export const parseIssues = (issues) => {
    if (issues === null) { return issues };

    if (issues.length === 0) {
        return 'No Issues'
    }
    
    if (issues.includes(true)) {
        issues = ['No Link']
    }

    return issues
}

/**
 * The function `filterSeekersByProject` filters a given data object by project and issue type,
 * returning a new object with the filtered data.
 * @param data - The `data` parameter is an object that represents a collection of seekers and their
 * projects. Each seeker is represented by a key in the `data` object, and the value associated with
 * each key is another object that represents the seeker's projects. Each project is represented by a
 * key in the inner object
 * @param whatGoes - The `whatGoes` parameter is an object that represents the projects that should be
 * included in the filtered result. The keys of the object represent the project names, and the values
 * can be any truthy value. If a project is not included in the `whatGoes` object, it will
 * @param issueType - The issueType parameter is used to filter the seekers based on the type of issue
 * they have. If the issueType is set to 'all', it will include all types of issues. Otherwise, it will
 * only include seekers who have the specified issueType.
 * @returns an object that contains filtered data based on the provided parameters.
 */
export const filterSeekersByProject = (data, whatGoes, issueType) => {

    let res = {};

    for (let seeker in data) {
        let addSeeker = false;

        for (let proj in data[seeker]) {
            if (!whatGoes[proj]) continue;
            let issues = data[seeker][proj];
            let issueTypes = Object.keys(issues);

            if (issueType !== 'all' && !issueTypes.includes(issueType)) {
                continue
            }

            if (issueTypes.length !== 0) {
                addSeeker = true;
            }

            if (addSeeker) {
                if (res[seeker] === undefined) {
                    res[seeker] = {email: data[seeker].email}
                }
                res[seeker][proj] = issues;
            }
        }
    }

    return res;
}





