/**
 * The function `assignDangerLevel` takes an array of issues and returns a string indicating the danger
 * level based on the issues.
 * @param issues - An array of issues. Each issue can be a number or a string representing a number.
 * @returns The function `assignDangerLevel` returns a string representing the danger level based on
 * the given `issues` array. The possible return values are:
 * - `'seeker-mid'` if any of the issues in the array matches the regular expression pattern
 * `^\d{0,4}\.\d+$`.
 * - `'seeker-good'` if the `issues` array is empty.
 * - `'
 */
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