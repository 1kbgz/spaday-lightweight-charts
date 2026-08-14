# Why Lightweight Charts uses a wrapper component

Lightweight Charts exposes an imperative JavaScript API rather than custom elements. Spaday, by
contrast, sends serializable component trees to a browser runtime. The wrapper reconciles these models
at one narrow boundary.

The `<lightweight-chart>` element owns the chart instance and translates property assignments into
library calls. Python still authors ordinary serializable props, while canvas creation, series changes,
resizing, and redraws remain in the browser where they belong.

This boundary also preserves live chart state. Updating `data` calls `setData()` on the existing series;
it does not replace the element. After the initial fit, the wrapper restores the visible logical range
so a streaming update does not reset a user's zoom.

A direct JavaScript integration can expose more of the upstream API, but every application would then
need its own lifecycle and spaday-property bridge. The package deliberately exposes only stable,
serializable inputs. Applications that need an upstream feature not represented here can extend the
custom element without changing spaday core.
