import hyperchamber as hc
import inspect


class ValidationException(Exception):
    """
    GAN components validate their configurations before creation.  
    
    `ValidationException` occcurs if they fail.
    """
    pass

class GANComponent:
    """
    GANComponents are pluggable pieces within a GAN.

    GAN objects are also GANComponents.
    """
    def __init__(self, gan, config):
        """
        Initializes a gan component based on a `gan` and a `config` dictionary.

        Different components require different config variables.  

        A `ValidationException` is raised if the GAN component configuration fails to validate.
        """
        self.gan = gan
        self.config = hc.Config(config)
        errors = self.validate()
        if errors != []:
            raise ValidationException("\n".join(errors))
        self.create_ops(config)

    def create_ops(self, config):
        """
        Create the ops object as `self.ops`.  Also looks up config TODO: review
        """
        if self.gan is None:
            return
        if self.gan.ops_backend is None:
            return
        self.ops = self.gan.ops_backend(config=self.config, device=self.gan.device)
        self.config = self.ops.lookup(config)

    def required(self):
        """
        Return a list of required config strings and a `ValidationException` will be thrown if any are missing.

        Example: 
        ```python
            class MyComponent(GANComponent):
                def required(self):
                    "learn rate is required"
                    ["learn_rate"]
        ```
        """
        return []

    def validate(self):
        """
        Validates a GANComponent.  Return an array of error messages. Empty array `[]` means success.
        """
        errors = []
        required = self.required()
        for argument in required:
            if(self.config.__getattr__(argument) == None):
                errors.append("`"+argument+"` required")

        if(self.gan is None):
            errors.append("GANComponent constructed without GAN")
        return errors

    def weights(self):
        """
            The weights of the GAN component.
        """
        return self.ops.weights

    def biases(self):
        """
            Biases of the GAN component.
        """
        return self.ops.biases

    def variables(self):
        """
            All variables associated with this component.
        """
        return self.ops.variables()

    def split_batch(self, net):
        """ 
        Discriminators return stacked results (on axis 0).  
        
        This splits the results.  Returns [d_real, d_fake]
        """
        ops = self.ops
        s = ops.shape(net)
        bs = s[0]
        net = ops.reshape(net, [bs, -1])
        size = [bs//2] + [x for x in ops.shape(net)[1:]]
        start = [0 for x in ops.shape(net)]
        start2 = [bs//2] + [0 for x in ops.shape(net)[1:]]
        d_real = ops.slice(net, start, size)
        d_fake = ops.slice(net, start2, size)
        return [d_real, d_fake]

    def reuse(self, net):
        self.ops.reuse()
        net = self.build(net)
        self.ops.stop_reuse()
        return net
