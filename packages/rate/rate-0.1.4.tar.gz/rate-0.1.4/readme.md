## Rate
A Cli-tool for rating players from a file.
Supported Algorithms:
- [Elo](https://en.wikipedia.org/wiki/Elo_rating_system)
- [Glicko](https://en.wikipedia.org/wiki/Glicko_rating_system)
- [Glicko-2](https://en.wikipedia.org/wiki/Glicko-2_rating_system)
- [TrueSkill](https://en.wikipedia.org/wiki/TrueSkill)
- [DWZ](https://en.wikipedia.org/wiki/DWZ_rating_system)
- [ECF](https://en.wikipedia.org/wiki/ECF_grading_system)

## Usage
```
rate path/to/file.csv or path/to/file.json
```
And you will get prompted with interactive options to select:
- First player key in the file
- Second player key in the file
- Result key from the first player perspective in the file
- Algorithm to use `[all, elo, "glicko-1", "glicko-2", "trueskill", "dwz", "ecf"]`
- Output Format `[csv, json]`
- How a win is defined in the file `Example`: `1` or `win` 
- How a loss is defined in the file `Example`: `0` or `loss` 
- How a draw is defined in the file `Example`: `0.5` or `draw` 
## Example
### matches.csv
| player1 | player2 | result1 | result2 | date       |
|---------|---------|---------|---------|------------|
| John    | Doe     | won     | Lost    | 12-14-2021 |
| Doe     | John    | Draw    | Draw    | 12-15-2021 |
| Sam     | John    | Lost    | won     | 12-16-2021 |
#### examples of generated files in /examples
### Answers
- First player key: player1
- Second player key: player2
- Result key: result1
- Algorithm: elo
- Output Format: csv
- How a win is defined: won
- How a loss is defined: Lost
- How a draw is defined: Draw

## Installation
```
$ pip install rate
$ rate
```
### or ###
```
$ py -m pip install rate
$ py -m rate
```
You might need to run it with `winpty` if you are on Windows.
```winpty py -m rate```

## Contributing
It still needs some work.
Please feel free to open an issue or pull request.