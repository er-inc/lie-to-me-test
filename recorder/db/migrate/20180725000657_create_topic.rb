class CreateTopic < ActiveRecord::Migration[5.1]
  def change
    create_table :topics do |t|
      t.string :title, null: false, unique: true
    end
  end
end
