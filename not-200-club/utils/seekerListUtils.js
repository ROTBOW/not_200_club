

export const assignDangerLevel = (issues) => {
    if (issues === null) { return '' };
    
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