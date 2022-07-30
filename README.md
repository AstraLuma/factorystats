# factorystats

## Schema (definitely not real SQL)


### Amelia thoughts: (3NF???)
```
CREATE TABLE __raw WITH COLUMNS (
    "time" INTEGER INDEX,
    "surface" INTEGER FOREIGN KEY __surfaces INDEX,
    "combinator" INTEGER FOREIGN KEY __combinators INDEX,
    "tags" HSTORE,
    "signal" INTEGER FOREIGN KEY __signals INDEX,
    "circuit" ENUM('red','green') NOT NULL,
    "value" INTEGER NOT NULL
)
CREATE TABLE __surfaces WITH COLUMNS (
    "index" INTEGER UNIQUE NOT NULL,
    "name" TEXT
)
CREATE TABLE __combinators WITH COLUMNS (
    "index" PRIMARY KEY AUTO INTEGER UNIQUE NOT NULL,
    "name" TEXT
)
CREATE TABLE __signals WITH COLUMNS (
    "index" PRIMARY KEY AUTO INTEGER UNIQUE NOT NULL,
    "name" TEXT
)
```

### Jamie thoughts:
```
CREATE TABLE __ raw WITH COLUMNS (
    "time" INTEGER INDEX,
    "surface" ???? INDEX,
    "combinator_name" TEXT,
    "tags" HSTORE, // 'type' => 'production', 'factory' => 'tmsc'
    "circuit" ENUM('red','green') NOT NULL,
    "signals" HSTORE // 'iron-plate' => 1234, 'copper-plate' => 5678
)
```

INSERT each JSON struct as a row, discarding the `unit_number` but keeping separate structs separate rows

### Other thoughts:

Pivot to make columns for signals

## How to fix time?
* Virtual column for time, started from NOW() working backwards?
* View with an externally-updated moving epoch, working forward?
  * forwarder has `ticks` which is pretty much guaranteed to be latest
  * since `now()` is definitionally latest, `epoch` is `now().shift(seconds=-ticks/60.0)`
  * `time` is `ticks / 60.0` (if float), or `ticks * 1000/60.0` if that makes happier indicies
  * (it probably does)
* Magic?