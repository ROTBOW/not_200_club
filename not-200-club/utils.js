export const parseIssues = (issues) => {
    if (issues.length === 0) {
        return 'No Issues'
    }
    
    if (issues.includes(true)) {
        issues = ['No Link']
    }

    return issues
}