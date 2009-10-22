def setSelectWidget(browser, name, labels):
    """Selects the given labels from a named SelectWidget control. (A
    functional replacement for the JavaScript used by this widget.)
    """
    control = browser.getControl(name='%s.from' % name).mech_control
    form = control._form
    for label in labels:
        value = str(control.get(label=label))
        form.new_control('text', name, {'value': value})

