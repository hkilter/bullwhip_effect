class Knn
   def initialize
       @data = []
       @id_to_position = {}
       @position_to_id
   end

   def add_instance(instance_data, id)
       @data << instance_data
       position = @data.length - 1
       @id_to_position[id] = position
       @position_to_id[position] = id
   end

   def get instance_for_id(id)
       @data[@id_to_position[id]]
   end
end