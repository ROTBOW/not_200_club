

export const assignDangerLevel = (issues) => {
    if (issues === null) { return '' };
    console.log(issues);
    for (let issue of issues) {
        const re = /^\d{0,4}\.\d+$/;
        if (re.test(issue.toString())) {
            return 'seeker-mid'
        }
    }

    if (issues.length === 0) {
        return 'seeker-good'
    }

    return 'seeker-bad'
}

export const filterSeekersByProject = (data, whatGoes) => {
    let res = {};

    for (let seeker in data) {
        let addSeeker = false;

        for (let proj in data[seeker]) {
            if (!whatGoes[proj]) continue;
            let issues = data[seeker][proj]
            if (Object.keys(issues).length !== 0) {
                addSeeker = true;
            }

            if (addSeeker) {
                if (res[seeker] === undefined) {
                    res[seeker] = {}
                }
                res[seeker][proj] = issues;
            }
        }
    }

    return res;
}