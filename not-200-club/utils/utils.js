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





