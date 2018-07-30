class Topic < ApplicationRecord
  validates :title, uniqueness: true
end
