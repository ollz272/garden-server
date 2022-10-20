NOTE - this project is very much geared towards my setup. You may find you need to make adjustments. I have only tested this on MacOSX

For production running, we also require an S3 bucket and Redis for caching.

## Development setup

It's recommended you use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/)
You will also need a locally running postgres database running. This _can_ be changed to sqlite but requires updating the settings.

Presuming you are using those tools, getting started on this project is pretty straightforward:

```console
$ mkproject --force --python=3.10 garden_server
$ workon gardenserver
$ make reset
```


You can now run the development server:

```console
$ python manage.py runserver
```

## Usage
Login as `admin@admin.com` with password `password`, and you should be able to get started.
You can create new plants to be tracked with at:
`127.0.0.1:8000/plants/create/`

You can then post data points to:
`127.0.0.1:8000/api/plant-data/`
With data, like:
```json
{"plant": 1, "data_type": 1, "data": "YOUR DATA HERE - MUST BE A NUMBER!"}
```

And view charts at:
`127.0.0.1:8000/plants/chart/{id}/`