# automate-lifx-plugin
[![Build Status](https://app.travis-ci.com/majamassarini/automate-lifx-plugin.svg?branch=main)](https://app.travis-ci.com/majamassarini/automate-lifx-plugin)
[![codecov](https://codecov.io/gh/majamassarini/automate-lifx-plugin/branch/main/graph/badge.svg?token=hGxVY2MzWP)](https://codecov.io/gh/majamassarini/automate-lifx-plugin)
[![Documentation Status](https://readthedocs.org/projects/automate-lifx-plugin/badge/?version=latest)](https://automate-lifx-plugin.readthedocs.io/en/latest/?badge=latest)

The **Lifx** plugin for the [automate-home project](https://github.com/majamassarini/automate-home).

## Yaml examples of usage

Trigger and commands for a [indoor hue light model](https://automate-home.readthedocs.io/en/latest/appliances.html#light-indoor-hue-appliance).
```yaml
- !Performer
  name: "lifx state"
  for appliance: "an indoor hue light"
  commands: []
  triggers:
    - !lifx_plugin.trigger.State
      addresses: [["172.31.10.245", 56700]]
      events: []


- !Performer
  name: "set color command"
  for appliance: "an indoor hue light"
  commands:
    - !lifx_plugin.command.SetColor { addresses: [ [ "172.31.10.245", 56700 ] ] }
  triggers: [ ]


- !Performer
  name: "start show command"
  for appliance: "an indoor hue light"
  commands:
    - !lifx_plugin.command.SetWaveform { addresses: [ [ "172.31.10.245", 56700 ] ] }
  triggers: [ ]


- !Performer
  name: "adjust lifx brightness through a knx dimming button"
  for appliance: "an indoor hue light"
  commands:
    - !lifx_plugin.command.SetColor {addresses: [["172.31.10.245", 56700]]}
  triggers:
    - !knx_plugin.trigger.dpt_control_dimming.BrightnessStep {addresses: [0x0C07]}
```

## Documentation

* [automate-home protocol commands/triggers chapter](https://automate-home.readthedocs.io/en/latest/performer.html)
* [automate-lifx-plugin documentation](https://automate-lifx-plugin.readthedocs.io/en/latest/?badge=latest)

## Contributing

Pull requests are welcome!

## License

The automate-lifx-plugin is licensed under MIT.