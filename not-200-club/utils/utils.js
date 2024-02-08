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





