# Change Log

竜 **TatSu** uses [Semantic Versioning](http://semver.org/) for its releases, so parts of the version number may increase without any significant changes or backwards incompatibilities in the software.

The format of this *Change Log* is inspired by [keeapachangelog.org](http://keepachangelog.com/).

## [X.Y.Z](https://github.com/apalala/tatsu/compare/v5.7.3...master) @ 2022

## [5.7.3](https://github.com/apalala/tatsu/compare/v5.7.2...v5.7.3) @ 2021-12-20

-   Fix that settings passed to `Context.parse()` were ignored. Add `Context.active_config` for the configuration active during a parse
-   Define `Node._parent` as part of the `@dataclass`

## [5.7.2](https://github.com/apalala/tatsu/compare/v5.7.1...v5.7.2) @ 2021-12-18

-   Make `AST` and `Node` hashable. Necessary for caching `Node.children()`
-   Implement `Node.__eq__()` in terms of identity or `Node.ast.__eq__()__`
-   Fix regression in which rule order is lost in generated parsers ([@dtrckd](https://github.com/dtrckd))
-   Restore `Node.ast` (was removed because of problems with `__eq__()`)
-   Get `Node.children()` from `Node.ast` when there are no attributes defined for the `Node`. This restores the desired behavior while developing a parse model.

## [5.7.1](https://github.com/apalala/tatsu/compare/v5.6.1...v5.7.1) @ 2021-12-03

-   Simplified this CHANGELOG by not linking to issues or and pull requests that can be queried on Github
-   Now `config: ParserConfig` is used in `__init__()` and `parse()` methods of `contexts.ParseContext`, `grammars.Grammar`, and elsewhere to avoid long parameter lists. `ParserConfig` also provides clean and clear ways of overridinga group of settings
-   All names defined in the successful choice in a rule are now defined in the resulting [AST](http://en.wikipedia.org/wiki/Abstract_syntax_tree). Names within optionals that did not match will have their values set to `None`, and closures that did not match will be set to `[]`
-   Moved build configuration from `setup.py` in favor of `setup.cfg` and `pyproject.toml` ([@KOLANICH](https://github.com/KOLANICH))
-   `Node.children()` is now computed only when required, and cached
-   Classes in generated object models are now `@dataclass`
-   Optimize and get rid of bugs and annoyances while keeping backwards compatibility
-   Drop support for Python \< 3.10

## [5.6.1](https://github.com/apalala/tatsu/compare/v5.6.0...v5.6.1) @ 2021-03-22

-   Fix bug in which rule fields were forced on empty `AST` ([@Victorious3](https://github.com/Victorious3))

## [5.6.0](https://github.com/apalala/tatsu/compare/v5.5.0...v5.6.0) @ 2021-03-21

-   Several important refactorings in `contexts.ParseContext`
-   Make `ignorecase` settings apply to defined `@@keywords`
-   Move checking of keywords used as names into `ParseContext`
-   Output of generated parsers again matches that of model parsers
-   Improve *"expecting one of:"* messages so elements are in declaration order
-   Stop code generation if there are closures over possibly empty expressions
-   Preserve name declaration order in returned `AST`
-   Update the bootstrap parser (`tatsu/bootstrap.py`) to the generated parser
-   Now generated parser's `main()` only outputs the JSON for the parse `AST`
-   Minor version bumped in case the many fixes break backwards-compatibility
-   Minor documentation issues fixed
-   All tests run with Python 3.8, 3.9, 3.10

## [5.5.0](https://github.com/apalala/tatsu/compare/v5.0.0...v5.5.0) @ 2020-01-26

-   [#156](https://github.com/neogeny/TatSu/issues/156) Clarify limitations of left-recursion in PEG ([@apalala](https://github.com/apalala))
-   [#159](https://github.com/neogeny/TatSu/pull/159) Clean up examples and tutorial, upgrade them to Python 3 ([@okomarov](https://github.com/okomarov))

## [5.0.0](https://github.com/apalala/tatsu/compare/v4.4.0...v5.0.0) @ 2020-01-26

-   竜 **TatSu** is now only tested against Python 3.8. Earlier versions of Python are now deprecated, and Python 2.X versions are no longer supported.
-   Apply `nameguard` only if `token[0].isalpha()`. This solves a regression afecting previous TatSu and Grako grammars ([@apalala](https://github.com/apalala)).
-   Remove `pygraphviz` from develoment requirements, as it doesn't build under Py38
-   [#56](https://github.com/neogeny/TatSu/issues/56) Include missing `tatsu/g2e/antlr.ebnf` in distribution
-   [#138](https://github.com/neogeny/TatSu/issues/138) Reimplement the calculation of `FIRST`, `FOLLOW`, and `LOOKAHEAD` sets using latest theories. For now, this should improve parser error reporting, but should eventually enable the simplification of parsing of leftrec grammars ([@apalala](https://github.com/apalala)).
-   [#153](https://github.com/neogeny/TatSu/issues/153) Import ABCs from `collections.abc` ([@tirkarthi](https://github.com/tirkarthi))
-   The AST for sequences is now a `tuple` (it used to be a `list`-derived `closure`)

## [4.4.0](https://github.com/apalala/tatsu/compare/v4.3.0...v4.4.0) @ 2019-04-22

-   The default regexp for whitespace was changed to `(?s)\s+`
-   Allow empty patterns (`//`) like Python does
-   [#65](https://github.com/neogeny/TatSu/issues/65) Allow initial, consecutive, and trailing `@namechars`
-   [#73](https://github.com/neogeny/TatSu/issues/73) Allow `@@whitespace :: None` and `@@whitespace :: False`
-   [#75](https://github.com/neogeny/TatSu/issues/75) Complete implemenation of left recursion ([@Victorious3](https://github.com/Victorious3))
-   [#77](https://github.com/neogeny/TatSu/issues/77) Allow `@keyword` throughout the grammar
-   [#89](https://github.com/neogeny/TatSu/issues/89) Make all attributes defined in the rule present in the resulting `AST` or `Node` even if the associated expression was not parsed
-   [#93](https://github.com/neogeny/TatSu/issues/93) Fix trace colorization on Windows
-   [#96](https://github.com/neogeny/TatSu/issues/96) Documented each `@@directive`
-   Switched the documentation to the "Alabaster" theme
-   Various code and documentation fixes ([@davesque](https://github.com/davesque), [@nicholasbishop](https://github.com/nicholasbishop), [@rayjolt](https://github.com/rayjolt))

## [4.3.0](https://github.com/apalala/tatsu/compare/v4.2.6...v4.3.0) @ 2018-11-17

-   [#66](https://github.com/neogeny/TatSu/issues/66) Fix multiline ( `(?x)` ) patterns not properly supported in grammar ([@pdw-mb](https://github.com/pdw-mb))
-   [#70](https://github.com/neogeny/TatSu/issues/70) Important upgrade to `ModelBuilder` and grammar specification of classes for generated nodes. See [pull request #78](https://github.com/neogeny/TatSu/pull/78) for details ([@Victorious3](https://github.com/Victorious3))

## [4.2.6](https://github.com/apalala/tatsu/compare/v4.2.5...v4.2.6) @ 2018-05-06

-   [#56](https://github.com/neogeny/TatSu/issues/56) Add missing `tatsu/g2e/antlr.ebnf` to distribution ([@Ruth-Polymnia](https://github.com/Ruth-Polymnia))
-   [#62](https://github.com/neogeny/TatSu/issues/62) Fix 竜 **TatSu** ignoring start rule provided in command line ([@r-chaves](https://github.com/r-chaves))
-   Fix typos in documentation ([@mjdominus](https://github.com/mjdominus))

## [4.2.5](https://github.com/apalala/tatsu/compare/v4.2.4...v4.2.5) @ 2017-11-26

-   [#42](https://github.com/neogeny/TatSu/issues/42) Rename vim files from `grako.vim` to `tatsu.vim` ([@fcoelho](https://github.com/fcoelho))
-   [#51](https://github.com/neogeny/TatSu/issues/51) Fix inconsistent code generation for `whitespace` ([@fpom](https://github.com/fpom))
-   [#54](https://github.com/neogeny/TatSu/pull/54) Only care about case of first letter of rule name for determining advance over whitespace ([@acw1251](https://github.com/acw1251))

## [4.2.4](https://github.com/apalala/tatsu/compare/v4.2.3...v4.2.4) @ 2017-07-10

### Fixed

-   [#40](https://github.com/neogeny/TatSu/issues/40) Make the start rule default to the first rule defined in the grammar ([@hariedo](https://github.com/hariedo))
-   [#43](https://github.com/neogeny/TatSu/issues/43) Import 're' from tatsu.util to support optional 'regex'-only features ([@azazel75](https://github.com/azazel75))
-   [#47](https://github.com/neogeny/TatSu/issues/47) Fix incorrect sample code in documentation ([@apalala](https://github.com/apalala))

## [4.2.3](https://github.com/apalala/tatsu/compare/v4.2.2...v4.2.3) @ 2017-07-10

### Fixed

-   [#37](https://github.com/neogeny/TatSu/issues/37) Regression: The `#include` pragma works by using the `EBNFBuffer` from `grammars.py`. Somehow the default `EBNFBootstrapBuffer` from `bootstrap.py` has been used instead ([@gegenschall](https://bitbucket.org/gegenschall)).
-   [#38](https://github.com/neogeny/TatSu/issues/38) Documentation: Use of `json.dumps()` requires `ast.asjson()` ([@davidchen](https://github.com/davidchen)).

## [4.2.2](https://github.com/apalala/tatsu/compare/v4.2.1...v4.2.2) @ 2017-07-01

### Fixed

-   [#27](https://github.com/neogeny/TatSu/issues/27) Undo the fixes to dropped input on left recursion because they broke previous expected behavior.
-   [#33](https://github.com/neogeny/TatSu/issues/33) Fixes to the calc example and mini tutorial ([@heronils](https://github.com/heronils))
-   [#34](https://github.com/neogeny/TatSu/issues/34) More left-recursion test cases ([@manueljacob](https://github.com/manueljacob)).

## [4.2.1](https://github.com/apalala/tatsu/compare/v4.2.0...v4.2.1) @ 2017-06-18

### Fixed

-   [#27](https://github.com/neogeny/TatSu/issues/27) Left-recursive parsers would drop or skip input on many combinations of grammars and correct/incorrect inputs([@manueljacob](https://github.com/manueljacob))
-   Documentation fixes ([@manueljacob](https://github.com/manueljacob), [@paulhoule](https://github.com/paulhoule))

## [4.2.0](https://github.com/apalala/tatsu/compare/v4.1.1...v4.2.0) @ 2017-05-21

### Added

-   Parse speeds on large files reduced by 5-20% by optimizing parse contexts and closures, and unifying the [AST](http://en.wikipedia.org/wiki/Abstract_syntax_tree) and [CST](https://en.wikipedia.org/wiki/Parse_tree) stacks.
-   Added the *"skip to"* expression ( `->`), useful for writing *recovery* rules. The parser will advance over input, one character at time, until the expression matches. Whitespace and comments will be skipped at each step.
-   Added the *any* expression ( `/./`) for matching the next character in the input.
-   The [ANTLR](http://www.antlr.org/) grammar for [Python3](http://python.org) to the `g2e` example, and udate `g2e` to handle more [ANTLR](http://www.antlr.org/) syntax.
-   Check typing with [Mypy](http://mypy-lang.org).

### Changed

-   Removed the very old \_[regex](https://pypi.python.org/pypi/regex) example.
-   Make parse traces more compact. Add a sample to the docs.
-   Explain [Grako](https://pypi.python.org/pypi/grako/) compatibility in docs.

## [4.1.1](https://github.com/apalala/tatsu/compare/v4.1.0...v4.1.1) @ 2017-05-21

### Fixed

-   `tatus.objectmodel.Node` not setting attributes from `AST`.

## [4.1.0](https://github.com/apalala/tatsu/compare/v4.0.0...v4.1.0) @ 2017-05-21

### Added

-   New support for *left recursion* with correct associativity. All test cases pass.
-   Left recursion is enabled by default. Use the `@@left_recursion :: False` directive to diasable it.
-   Renamed the decorator for generated rule methods to `@tatsumasu`.
-   Refactored the `tatsu.contexts.ParseContext` for clarity.
-   The `@@ignorecase` directive and the `ignorecase=` parameter no longer appy to regular expressions (patterns) in grammars. Use `(?i)` in the pattern to ignore the case in a particular pattern.
-   Now `tatsu.g2e` is a library and executable module for translating [ANTLR](http://www.antlr.org/) grammars to **TatSu**.
-   Modernized the `calc` example and made it part of the documentation as *Mini Tutorial*.
-   Simplified the generated object models using the semantics of class attributes in [Python](http://python.org)

## [4.0.0](https://github.com/apalala/tatsu/compare/0.0.0...v4.0.0) @ 2017-05-06

-   First release.
