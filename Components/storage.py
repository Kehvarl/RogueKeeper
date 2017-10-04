class Storage:
    def __init__(self, label, capacity):
        self.label = label
        self.capacity = capacity
        self.capacity_used = 0
        self.items = []
        self.resources = {}
        self.owner = None

    def add_resource(self, resource):
        """
        Store Resources in this container
        :param dict resource:
        :return:
        """
        results = []

        name, quantity = resource.items()[0]
        if self.capacity_used + quantity > self.capacity:
            results.append({
                'item_added': None,
                'message': 'Insufficient Storage for {0} {1}.  Storage remaining: {2}'.format(
                    quantity, name, self.capacity - self.capacity_used)
            })

        else:
            results.append({
                'item_added': resource,
                'message': '{0} {1} added to {2}'.format(quantity, name, self.label)
            })
            if name in self.resources:
                self.resources[name] += quantity
            else:
                self.resources[name] = quantity
            self.capacity_used += quantity

        return results

    def transfer_resources(self, other):
        """
        Transfer the contents of an other storage container to this one
        :param Storage other:
        :return:
        """
        results = []

        if self.capacity_used + other.capacity_used > self.capacity:
            results.append({
                'item_added': None,
                'message': 'Insufficient Storage for the contents of {0}'.format(other.label)
            })
        else:
            for resource in other.resources:
                results.extend(self.add_resource(resource))
        return results
